"""This module provides a client for watching videos on Niconico."""

from __future__ import annotations

import asyncio
import json
import re
import secrets
import string
import subprocess
import time
from pathlib import Path

import requests

from niconico.base.client import BaseClient
from niconico.decorators import login_required
from niconico.exceptions import CommentAPIError, DownloadError, NicoAPIError, WatchAPIError
from niconico.objects.nvapi import AccessRightsData, NvAPIResponse, ThreadKeyData
from niconico.objects.video.watch import (
    NvCommentAPIData,
    NvCommentAPIResponse,
    StoryboardResponse,
    WatchAPIData,
    WatchAPIErrorData,
    WatchAPIResponse,
    WatchData,
)


class VideoWatchClient(BaseClient):
    """A client for watching videos on Niconico."""

    def get_watch_data(self, video_id: str) -> WatchData:
        """Get the watch data of a video.

        Args:
            video_id: The ID of the video.

        Returns:
            WatchData | WatchResponseError: The watch data of the video if successful, WatchResponseError
        """
        res = self.niconico.get(f"https://www.nicovideo.jp/watch/{video_id}?responseType=json")
        if res.status_code == requests.codes.ok:
            res_cls_data = WatchAPIResponse[WatchAPIData](**res.json())
            return res_cls_data.data.response
        res_cls_error = WatchAPIResponse[WatchAPIErrorData](**res.json())
        raise WatchAPIError(response=res_cls_error.data.response)

    def generate_action_track_id(self) -> str:
        """Generate a random action track ID.

        Returns:
            str: The generated action track ID.
        """
        fh_chars = string.ascii_letters + string.digits
        fh = "".join(secrets.choice(fh_chars) for _ in range(10))
        lh = int(time.time() * 1000)
        return f"{fh}_{lh}"

    def get_outputs(self, watch_data: WatchData, *, audio_only: bool = False) -> dict[str, list[str]]:
        """Get the outputs of a video.

        Args:
            watch_data: The watch data of the video.
            audio_only: Whether to get the audio only.

        Returns:
            dict[str, list[str]]: The outputs of the video.
        """
        outputs: dict[str, list[str]] = {}
        top_audio_id = None
        top_audio_quality = -1
        for audio in watch_data.media.domand.audios:
            if audio.is_available and audio.quality_level > top_audio_quality:
                top_audio_id = audio.id_
                top_audio_quality = audio.quality_level
        if top_audio_id is None:
            return outputs
        for video in watch_data.media.domand.videos:
            if video.is_available:
                outputs[video.label] = [top_audio_id] if audio_only else [video.id_, top_audio_id]
        return outputs

    def get_hls_content_url(self, watch_data: WatchData, outputs: list[list[str]]) -> str | None:
        """Get the HLS content URL of a video.

        Args:
            watch_data: The watch data of the video.
            outputs: The outputs. e.g.: [video_id, audio_id][]

        Returns:
            str | None: The HLS content URL of the video if successful, None otherwise.
        """
        video_id = watch_data.client.watch_id
        action_track_id = watch_data.client.watch_track_id
        access_right_key = watch_data.media.domand.access_right_key
        res = self.niconico.post(
            f"https://nvapi.nicovideo.jp/v1/watch/{video_id}/access-rights/hls?actionTrackId={action_track_id}",
            json={"outputs": outputs},
            headers={"X-Access-Right-Key": access_right_key},
        )
        if res.status_code == requests.codes.created:
            res_cls = NvAPIResponse[AccessRightsData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.content_url
        return None

    @login_required(premium=True)
    def get_storyboard_url(self, watch_data: WatchData) -> str | None:
        """Get the storyboards URL of a video.

        Args:
            watch_data: The watch data of the video.

        Returns:
            str | None: The storyboards URL of the video if successful, None otherwise.
        """
        if not watch_data.media.domand.is_storyboard_available:
            return None
        video_id = watch_data.client.watch_id
        action_track_id = watch_data.client.watch_track_id
        access_right_key = watch_data.media.domand.access_right_key
        res = self.niconico.post(
            f"https://nvapi.nicovideo.jp/v1/watch/{video_id}/access-rights/storyboard?actionTrackId={action_track_id}",
            headers={"X-Access-Right-Key": access_right_key},
        )
        if res.status_code == requests.codes.created:
            res_cls = NvAPIResponse[AccessRightsData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.content_url
        return None

    @login_required(premium=True)
    def download_storyboards(self, watch_data: WatchData, output_path: str) -> str:
        """Download the storyboards of a video.

        Args:
            watch_data: The watch data of the video.
            output_path: The folder path to save the storyboards.

        Returns:
            str: The path of the downloaded storyboards.
        """
        storyboard_url = self.get_storyboard_url(watch_data)
        if storyboard_url is None:
            raise NicoAPIError(message="Failed to get the storyboards URL.")
        output_path = output_path % {
            "id": watch_data.video.id_,
            "title": watch_data.video.title,
            "owner": watch_data.owner.nickname,
            "owner_id": str(watch_data.owner.id_),
            "timestamp": str(int(time.time())),
        }
        res = self.niconico.get(storyboard_url)
        if res.status_code == requests.codes.ok:
            res_cls = StoryboardResponse(**res.json())
            if not Path(output_path).is_dir():
                Path(output_path).mkdir(parents=True)
            if Path(f"{output_path}/storyboard.json").exists():
                raise DownloadError(message="The storyboard.json file already exists.")
            with Path(f"{output_path}/storyboard.json").open(mode="w") as f:
                f.write(res.text)
            for image in res_cls.images:
                image_res = self.niconico.get(re.sub(r"(?<=/)[^/]+(?=\?)", image.url, storyboard_url))
                if image_res.status_code == requests.codes.ok:
                    if Path(f"{output_path}/{image.url}.jpg").exists():
                        raise DownloadError(message=f"The storyboard image already exists: {image.url}")
                    with Path(f"{output_path}/{image.url}.jpg").open(mode="wb") as f:
                        f.write(image_res.content)
                else:
                    raise DownloadError(message=f"Failed to download the storyboard image: {image.url}")
        else:
            raise DownloadError(message="Failed to download the storyboards.")
        return output_path

    def download_video(
        self,
        watch_data: WatchData,
        output_label: str,
        output_path: str = "%(title)s.%(ext)s",
        *,
        audio_only: bool = False,
    ) -> str:
        """Download a video.

        Args:
            watch_data: The watch data of the video.
            output_label: The output label of the video.
            output_path: The path to save the video.
            audio_only: Whether to download the audio only.

        Returns:
            str: The path of the downloaded video.
        """
        outputs = self.get_outputs(watch_data, audio_only=audio_only)
        if output_label not in outputs:
            raise DownloadError(message="The output label is not available.")
        hls_content_url = self.get_hls_content_url(watch_data, [outputs[output_label]])
        if hls_content_url is None:
            raise NicoAPIError(message="Failed to get the HLS content URL.")
        output_path = output_path % {
            "id": watch_data.video.id_,
            "title": watch_data.video.title,
            "owner": watch_data.owner.nickname,
            "owner_id": str(watch_data.owner.id_),
            "timestamp": str(int(time.time())),
            "ext": "m4a" if audio_only else "mp4",
        }
        if not Path(output_path).parent.exists():
            Path(output_path).parent.mkdir(parents=True)
        if Path(output_path).exists():
            raise DownloadError(message="The video file already exists.")
        cookies = {
            "domand_bid": self.niconico.session.cookies.get("domand_bid"),
        }
        commands = " ".join(
            [
                "ffmpeg",
                "-headers",
                f"'cookie: {';'.join(f'{k}={v}' for k, v in cookies.items())}'",
                "-protocol_whitelist",
                "file,http,https,tcp,tls,crypto",
                "-i",
                f"'{hls_content_url}'",
                "-c",
                "copy",
                f"'{output_path}'",
            ],
        )
        try:
            with subprocess.Popen(  # noqa: S602
                commands,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True,
            ) as p:
                for line in iter(p.stdout.readline, b""):  # type: ignore[union-attr]
                    self.log("debug", line.rstrip())
                p.wait()
        except subprocess.CalledProcessError as e:
            raise DownloadError(message="Failed to download the video.") from e
        return output_path

    async def download_video_async(
        self,
        watch_data: WatchData,
        output_label: str,
        output_path: str = "%(title)s.%(ext)s",
        *,
        audio_only: bool = False,
    ) -> str:
        """Asynchronously download a video.

        Args:
            watch_data: The watch data of the video.
            output_label: The output label of the video.
            output_path: The path to save the video.
            audio_only: Whether to download the audio only.

        Returns:
            str: The path of the downloaded video.
        """
        outputs = self.get_outputs(watch_data, audio_only=audio_only)
        if output_label not in outputs:
            raise DownloadError(message="The output label is not available.")
        hls_content_url = self.get_hls_content_url(watch_data, [outputs[output_label]])
        if hls_content_url is None:
            raise NicoAPIError(message="Failed to get the HLS content URL.")
        output_path = output_path % {
            "id": watch_data.video.id_,
            "title": watch_data.video.title,
            "owner": watch_data.owner.nickname,
            "owner_id": str(watch_data.owner.id_),
            "timestamp": str(int(time.time())),
            "ext": "m4a" if audio_only else "mp4",
        }
        if not Path(output_path).parent.exists():
            Path(output_path).parent.mkdir(parents=True)
        if Path(output_path).exists():
            raise DownloadError(message="The video file already exists.")
        cookies = {
            "domand_bid": self.niconico.session.cookies.get("domand_bid"),
        }
        commands = " ".join(
            [
                "ffmpeg",
                "-headers",
                f"'cookie: {';'.join(f'{k}={v}' for k, v in cookies.items())}'",
                "-protocol_whitelist",
                "file,http,https,tcp,tls,crypto",
                "-i",
                f"'{hls_content_url}'",
                "-c",
                "copy",
                f"'{output_path}'",
            ],
        )
        try:
            process = await asyncio.create_subprocess_shell(
                commands,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
            )
            async for line in process.stdout:  # type: ignore[union-attr]
                self.log("debug", line.decode().rstrip())
            await process.wait()
        except Exception as e:
            raise DownloadError(message="Failed to download the video.") from e
        return output_path

    def get_thread_key(self, video_id: str) -> str | None:
        """Get the thread key of a video.

        Args:
            video_id: The ID of the video.

        Returns:
            str: The thread key of the video.
        """
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/comment/keys/thread?videoId={video_id}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[ThreadKeyData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.thread_key
        return None

    def get_comments(
        self,
        watch_data: WatchData,
        *,
        when: int | None = None,
        thread_key: str | None = None,
    ) -> NvCommentAPIData | None:
        """Get the comments of a video.

        Args:
            watch_data: The watch data of the video.
            when: The time to get the comments.
            thread_key: The thread key of the video.

        Returns:
            list[Any]: The comments of the video.
        """
        payload = {
            "threadKey": watch_data.comment.nv_comment.thread_key,
            "params": watch_data.comment.nv_comment.params.model_dump(by_alias=True),
            "additionals": {},
        }
        if when is not None:
            if self.niconico.premium:
                payload["additionals"] = {"when": when}
            else:
                raise NicoAPIError(message="You must be a premium member to get the comments at a specific time.")
        if thread_key is not None:
            payload["threadKey"] = thread_key
        res = self.niconico.post(
            watch_data.comment.nv_comment.server + "/v1/threads",
            data=json.dumps(payload),
        )
        res_cls = NvCommentAPIResponse(**res.json())
        if res_cls.meta.status == requests.codes.ok:
            return res_cls.data
        raise CommentAPIError(message=res_cls.meta.error_code)
