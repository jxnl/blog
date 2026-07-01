(function () {
  var snapshot;

  function loadSnapshot() {
    if (!snapshot) {
      snapshot = fetch("/assets/page-views.json", { credentials: "same-origin" })
        .then(function (response) {
          if (!response.ok) throw new Error("page-view snapshot unavailable");
          return response.json();
        })
        .then(function (data) {
          return data.views || {};
        })
        .catch(function () {
          return {};
        });
    }
    return snapshot;
  }

  function normalizePath(value) {
    var path = new URL(value, window.location.origin).pathname;
    if (path.endsWith("/index.html")) path = path.slice(0, -"index.html".length);
    if (path !== "/" && !path.endsWith("/")) path += "/";
    return path;
  }

  function formatViews(count) {
    return (
      new Intl.NumberFormat("en", {
        notation: "compact",
        maximumFractionDigits: 1,
      }).format(count) + " views"
    );
  }

  function renderPostPage(views) {
    var container = document.querySelector(".md-content--post");
    if (!container || container.querySelector(".page-view-count")) return;

    var count = views[normalizePath(window.location.pathname)];
    var heading = container.querySelector("article.md-content__inner > h1");
    if (!count || !heading) return;

    var element = document.createElement("p");
    element.className = "page-view-count";
    element.textContent = formatViews(count);
    heading.insertAdjacentElement("afterend", element);
  }

  function renderPostListings(views) {
    document.querySelectorAll("article.md-post--excerpt").forEach(function (post) {
      if (post.querySelector(".md-meta__item--views")) return;

      var link = post.querySelector(".md-post__content h2 a[href]");
      var metadata = post.querySelector(".md-meta__list");
      if (!link || !metadata) return;

      var count = views[normalizePath(link.href)];
      if (!count) return;

      var element = document.createElement("li");
      element.className = "md-meta__item md-meta__item--views";
      element.textContent = formatViews(count);
      metadata.appendChild(element);
    });
  }

  function renderPageViews() {
    loadSnapshot().then(function (views) {
      renderPostPage(views);
      renderPostListings(views);
    });
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(renderPageViews);
  } else {
    document.addEventListener("DOMContentLoaded", renderPageViews);
  }
})();
