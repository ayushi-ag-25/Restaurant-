
let currentIndex = 0; // current section
const sections = document.querySelectorAll("section");
let isScrolling = false; // lock

window.addEventListener("wheel", (e) => {
    if (isScrolling) return; // if already scrolling, ignore

    if (e.deltaY > 0 && currentIndex < sections.length - 1) {
        currentIndex++;
    } else if (e.deltaY < 0 && currentIndex > 0) {
        currentIndex--;
    } else {
        return; // no section to move, do nothing
    }

    isScrolling = true; // lock scrolling

    window.scrollTo({
        top: sections[currentIndex].offsetTop,
        behavior: "smooth"
    });

    // Unlock scroll after animation (~700ms)
    setTimeout(() => {
        isScrolling = false;
    }, 700); // adjust time according to smooth scroll speed
});
console.log('jiiiiii')
