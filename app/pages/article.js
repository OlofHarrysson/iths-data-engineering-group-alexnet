const articles = [
    {
      title: "AI News Article",
      description: "An article about AI news."
    }
  ];

  const articleList = document.querySelector(".article-List");
  const articleDetails = document.querySelector(".article-details");
  const articleTitle = document.querySelector("#article-title");
  const articleDescription = document.querySelector("#article-description");
  const closeDetailsButton = document.querySelector("#close-details");

  articles.forEach(article => {
    const articleElement = document.createElement("div");
    articleElement.classList.add("article");
    articleElement.innerHTML = `
      <h2>${article.title}</h2>
      <p>${article.description}</p>
      <button class="view-article">View article</button>
    `;
    articleList.appendChild(articleElement);

    const viewarticleButton = articleElement.querySelector(".view-article");
    viewarticleButton.addEventListener("click", () => {
      articleTitle.textContent = article.title;
      articleDescription.textContent = article.description;
      articleList.style.display = "none";
      articleDetails.style.display = "block";
    });

    closeDetailsButton.addEventListener("click", () => {
      articleDetails.style.display = "none";
      articleList.style.display = "flex";
    });
  });