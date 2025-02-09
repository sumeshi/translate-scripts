# translate-scripts
AI-Powered translation script samples.

```
$ ffmpeg -f lavfi -i color=c=black:s=1280x720 -i input.mp3 -vf "subtitles=input.srt" -c:v libx264 -c:a copy -shortest output.mp4
```