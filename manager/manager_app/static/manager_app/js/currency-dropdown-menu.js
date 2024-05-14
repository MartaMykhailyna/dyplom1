const root = document.documentElement;
const dropdownTitleIcon = document.querySelector(".dropdown-title-icon");
const dropdownTitle = document.querySelector(".dropdown-title");
const dropdownList = document.querySelector(".dropdown-list");
const mainButton = document.querySelector(".main-button");

const listItems = ["UAH", "EUR", "USD", "GBP"];

const iconTemplate = (path, viewBox) => {
  return `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="${viewBox}">
      <path d="${path}" />
    </svg>
  `;
};

const listItemTemplate = (currencyCode) => {
  return `
    <li class="dropdown-list-item">
      <a href="javascript:void(0);" onclick="changeCurrency('${currencyCode}')" class="dropdown-button list-button">
        <span class="text-truncate">${currencyCode}</span>
      </a>
    </li>
  `;
};

const renderListItems = () => {
  dropdownList.innerHTML += listItems
    .map((item) => {
      return listItemTemplate(item);
    })
    .join("");
};

window.addEventListener("load", () => {
  renderListItems();
});

const setDropdownProps = (deg, ht, opacity) => {
  root.style.setProperty("--rotate-arrow", deg !== 0 ? deg + "deg" : 0);
  root.style.setProperty("--dropdown-height", ht !== 0 ? ht + "rem" : 0);
  root.style.setProperty("--list-opacity", opacity);
};

mainButton.addEventListener("click", () => {
  const listWrapperSizes = 3.5; // margins, paddings & borders
  const dropdownOpenHeight = 4.6 * listItems.length + listWrapperSizes;
  const currDropdownHeight =
    root.style.getPropertyValue("--dropdown-height") || "0";

  currDropdownHeight === "0"
    ? setDropdownProps(180, dropdownOpenHeight, 1)
    : setDropdownProps(0, 0, 0);
});

dropdownList.addEventListener("click", (e) => {
  const clickedItemText = e.target.innerText.toLowerCase().trim();
  dropdownTitle.innerHTML = clickedItemText;
  setDropdownProps(0, 0, 0);
});
