let list = document.querySelectorAll(".navigation li");

function addHoverEffect() {
  this.classList.add("hovered");
}

function removeHoverEffect() {
  this.classList.remove("hovered");
}

// Attach both mouseover and mouseout events to each list item
list.forEach((item) => {
  item.addEventListener("mouseover", addHoverEffect);
  item.addEventListener("mouseout", removeHoverEffect);
});

// Menu Toggle
let toggle = document.querySelector(".toggle");
let navigation = document.querySelector(".navigation");
let main = document.querySelector(".main");

toggle.onclick = function () {
  navigation.classList.toggle("active");
  main.classList.toggle("active");
};

