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
    if (!container || container.querySelector(".md-nav__item--views")) return;

    var count = views[normalizePath(window.location.pathname)];
    var metadata = container.querySelector(".md-post__meta .md-nav__list");
    if (!count || !metadata) return;

    var element = document.createElement("li");
    element.className = "md-nav__item md-nav__item--views";

    var row = document.createElement("div");
    row.className = "md-nav__link";

    var icon = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    icon.setAttribute("viewBox", "0 0 24 24");

    var path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute(
      "d",
      "M12 9a3 3 0 1 0 0 6 3 3 0 0 0 0-6m0 8c-5 0-9.27-3.11-11-5 1.73-1.89 6-5 11-5s9.27 3.11 11 5c-1.73 1.89-6 5-11 5"
    );
    icon.appendChild(path);

    var label = document.createElement("span");
    label.className = "md-ellipsis";
    label.textContent = formatViews(count);

    row.appendChild(icon);
    row.appendChild(label);
    element.appendChild(row);
    metadata.appendChild(element);
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
