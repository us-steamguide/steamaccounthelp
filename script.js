document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("guideSearch");
  const articleGrid = document.getElementById("articleGrid");
  const resultCount = document.getElementById("resultCount");
  const emptyState = document.getElementById("emptyState");
  const clearButton = document.getElementById("clearSearch");
  const categoryButtons = Array.from(document.querySelectorAll(".category-chip"));
  const articleCards = articleGrid
    ? Array.from(articleGrid.querySelectorAll(".article-card"))
    : [];

  if (!searchInput || !articleGrid || !resultCount || !emptyState) {
    console.error("Steam Guide Hub: required search elements are missing.");
    return;
  }

  let selectedCategory = "All articles";

  function updateArticles() {
    const query = searchInput.value.trim().toLocaleLowerCase();
    let visibleCount = 0;

    articleCards.forEach((card) => {
      const category = card.dataset.category || "";
      const searchableText = (
        card.dataset.search || card.textContent || ""
      ).toLocaleLowerCase();

      const matchesCategory =
        selectedCategory === "All articles" ||
        category === selectedCategory;
      const matchesSearch = query === "" || searchableText.includes(query);
      const isVisible = matchesCategory && matchesSearch;

      card.hidden = !isVisible;
      if (isVisible) visibleCount += 1;
    });

    resultCount.textContent =
      `Showing ${visibleCount} ${visibleCount === 1 ? "guide" : "guides"}`;
    emptyState.hidden = visibleCount !== 0;
  }

  categoryButtons.forEach((button) => {
    button.addEventListener("click", () => {
      selectedCategory = button.dataset.filter || "All articles";

      categoryButtons.forEach((item) => {
        const active = item === button;
        item.classList.toggle("active", active);
        item.setAttribute("aria-pressed", String(active));
      });

      updateArticles();
    });

    button.setAttribute(
      "aria-pressed",
      String(button.classList.contains("active"))
    );
  });

  searchInput.addEventListener("input", updateArticles);

  if (clearButton) {
    clearButton.addEventListener("click", () => {
      searchInput.value = "";
      updateArticles();
      searchInput.focus();
    });
  }

  updateArticles();
});
