<!-- this will install flowplayer inside previous A- tag. -->
<script>
    flowplayer("a.player", "{{ MEDIA_URL }}flowplayer/flowplayer-3.2.7.swf", {
        clip: {
            autoPlay: false,
            autoBuffering: true, 
			scaling: "fit"
        }
    });
</script>