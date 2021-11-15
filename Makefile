landscape.mp4:
	ffmpeg -framerate 24 -i "img/%d.png" -vf "format=yuv420p,scale=1920:1200" output.mp4

clean:
	rm img/*.png
