const header = document.querySelector(".site-header");
const toggle = document.querySelector(".menu-toggle");
const nav = document.querySelector(".nav");
addEventListener(
  "scroll",
  () => header?.classList.toggle("solid", scrollY > 24),
  { passive: true },
);
toggle?.addEventListener("click", () => {
  const open = nav.classList.toggle("open");
  document.body.classList.toggle("menu-open", open);
  toggle.setAttribute("aria-expanded", open);
});
document.querySelectorAll(".nav a").forEach((a) =>
  a.addEventListener("click", () => {
    nav.classList.remove("open");
    document.body.classList.remove("menu-open");
  }),
);
const observer = new IntersectionObserver(
  (entries) =>
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      }
    }),
  { threshold: 0.12 },
);
document.querySelectorAll(".reveal").forEach((el) => observer.observe(el));
const form = document.querySelector("#enquiry-form");
form?.addEventListener("submit", (e) => {
  e.preventDefault();
  const data = new FormData(form);
  const msg = `Hello Your Phenomenal Builder, my name is ${data.get("name")}. I would like to discuss ${data.get("project")}. ${data.get("message")}`;
  location.href = `https://wa.me/263789411117?text=${encodeURIComponent(msg)}`;
});

const hero = document.querySelector(".hero");
if (
  hero &&
  matchMedia("(pointer:fine)").matches &&
  !matchMedia("(prefers-reduced-motion:reduce)").matches
) {
  hero.addEventListener("pointermove", (event) => {
    const x = event.clientX / innerWidth - 0.5;
    const y = event.clientY / innerHeight - 0.5;
    hero.querySelectorAll("[data-depth]").forEach((element) => {
      const depth = Number(element.dataset.depth);
      element.style.translate = `${x * depth}px ${y * depth}px`;
    });
  });
  hero.addEventListener("pointerleave", () => {
    hero.querySelectorAll("[data-depth]").forEach((element) => {
      element.style.translate = "0 0";
    });
  });
}
