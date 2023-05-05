const YTPlayerOverlay = document.querySelector(".overlay");
const YTlinks = document.querySelectorAll(".youtubelink");

YTlinks.forEach((link) => {
	link.addEventListener("click", () => {
		YTPlayerOverlay.classList.add("active");
	});
});

YTPlayerOverlay.addEventListener("click", () => {
	YTPlayerOverlay.classList.remove("active");
});
	
