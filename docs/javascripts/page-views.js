(function () {
  var snapshot;
  var feed;

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

  function loadFeed() {
    if (!feed) {
      feed = fetch("/feed_json_created.json", { credentials: "same-origin" })
        .then(function (response) {
          if (!response.ok) throw new Error("post feed unavailable");
          return response.json();
        })
        .then(function (data) {
          return data.items || [];
        })
        .catch(function () {
          return [];
        });
    }
    return feed;
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

  function formatDate(value) {
    if (!value) return "";

    return new Intl.DateTimeFormat("en", {
      year: "numeric",
      month: "short",
      day: "numeric",
    }).format(new Date(value));
  }

  function textFromHtml(value) {
    var element = document.createElement("div");
    element.innerHTML = value || "";
    return element.textContent.trim();
  }

  function getPostLink(post) {
    return post.querySelector(".md-post__content h2 a[href]");
  }

  function getPostViewCount(post, views) {
    var link = getPostLink(post);
    if (!link) return 0;
    return views[normalizePath(link.href)] || 0;
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
      post.setAttribute("data-page-views", String(getPostViewCount(post, views)));

      if (post.querySelector(".md-meta__item--views")) return;

      var metadata = post.querySelector(".md-meta__list");
      if (!metadata) return;

      var count = Number(post.getAttribute("data-page-views") || 0);
      if (!count) return;

      var element = document.createElement("li");
      element.className = "md-meta__item md-meta__item--views";
      element.textContent = formatViews(count);
      metadata.appendChild(element);
    });
  }

  function renderPopularItem(post) {
    var item = document.createElement("li");
    item.className = "popular-post";

    var header = document.createElement("div");
    header.className = "popular-post__header";

    var title = document.createElement("a");
    title.className = "popular-post__title";
    title.href = post.path;
    title.textContent = post.title;

    var views = document.createElement("span");
    views.className = "popular-post__views";
    views.textContent = formatViews(post.views);

    header.appendChild(title);
    header.appendChild(views);
    item.appendChild(header);

    var meta = document.createElement("div");
    meta.className = "popular-post__meta";
    meta.textContent = formatDate(post.date);
    item.appendChild(meta);

    if (post.description) {
      var description = document.createElement("p");
      description.className = "popular-post__description";
      description.textContent = post.description;
      item.appendChild(description);
    }

    return item;
  }

  function renderPopularPage(views) {
    var container = document.querySelector("[data-popular-posts]");
    if (!container) return;

    loadFeed().then(function (items) {
      if (!container.isConnected) return;

      var posts = items
        .map(function (item) {
          var path = normalizePath(item.url || item.id);
          return {
            date: item.date_published || item.date_modified,
            description: textFromHtml(item.content_html),
            path: path,
            title: item.title,
            views: views[path] || 0,
          };
        })
        .filter(function (item) {
          return item.title && item.path && item.views;
        })
        .sort(function (first, second) {
          if (first.views !== second.views) return second.views - first.views;
          return new Date(second.date) - new Date(first.date);
        });

      container.textContent = "";

      if (!posts.length) {
        var empty = document.createElement("p");
        empty.className = "popular-posts__status";
        empty.textContent = "Popular posts will appear here once page-view data is available.";
        container.appendChild(empty);
        return;
      }

      var list = document.createElement("ol");
      list.className = "popular-posts__list";

      posts.forEach(function (post) {
        list.appendChild(renderPopularItem(post));
      });

      container.appendChild(list);
    });
  }

  function renderPageViews() {
    loadSnapshot().then(function (views) {
      renderPostPage(views);
      renderPostListings(views);
      renderPopularPage(views);
    });
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(renderPageViews);
  } else {
    document.addEventListener("DOMContentLoaded", renderPageViews);
  }
})();
