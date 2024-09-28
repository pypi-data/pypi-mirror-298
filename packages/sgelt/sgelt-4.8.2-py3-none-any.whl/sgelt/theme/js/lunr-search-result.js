function lunr_search(term) {
  if (!lunr_index) {
    console.error("lunr index is required");
    return;
  }

  const items = lunr_index["pages"];
  const documents = lunr_index["pages"];
  let counter = 0;

  for (item in documents) {
    documents[item]["id"] = counter;
    counter = counter + 1;
  }

  idx = lunr(function () {
    this.ref("id");
    this.field("title");
    this.field("url");
    this.field("text", { boost: 10 });
    this.field("tags");
    this.field("date");

    items.forEach(function (doc) {
      this.add(doc);
    }, this);
  });

  if (term && idx && documents) {
    const resultHeadingRoot = document.getElementById(
      "lunr-search-result-heading"
    );
    const resultIntro = `
    <h1>Résultats pour <code>${term}</code></h1>
    `;

    resultHeadingRoot.insertAdjacentHTML("beforeend", resultIntro);

    const resultRoot = document.getElementById("lunr-search-result");
    const collection = document.createElement("div");
    collection.classList.add('collection');

    const searchQueryRegex = new RegExp(createQueryStringRegex(term), "gmi");
    //put results on the screen.
    var results = idx.search(term);
    if (results.length > 0) {
      //if results
      for (var i = 0; i < results.length; i++) {
        var ref = results[i]["ref"];
        var url = documents[ref]["url"];
        var title = documents[ref]["title"].replace(searchQueryRegex, "<strong>$&</strong>");
        var body = documents[ref]["text"].substring(0, 280).replace(searchQueryRegex, "<strong>$&</strong>") + "...";
        var tags = documents[ref]["tags"];
        var date = documents[ref]["date"];

        const resultItem = `
          <a class="collection-item lunr-search-result" href=${url}>
          <span class="badge">${date}</span>
            <h3 class="title">${title}</h3>
            <p class="lunr-search-result-item-body">${body}
            </p>
            <div class="chip">${tags}</div>
          </a>
          `;

          collection.insertAdjacentHTML("beforeend", resultItem);
      }
    } else {
      const resultFailure = `<div class="collection-item lunr-search-result"><p class="lunr-result-fail">&#x2205;</p></div>`;
      collection.insertAdjacentHTML("beforeend", resultFailure);
    }
    resultRoot.appendChild(collection);
  }
  return false;
}

function createQueryStringRegex(query) {
  const searchTerms = query.split(" ");
  if (searchTerms.length == 1) {
    return query;
  }
  query = "";
  for (const term of searchTerms) {
    query += `${term}|`;
  }
  query = query.slice(0, -1);
  return `(${query})`;
}

function getQueryVariable(variable) {
  var query = window.location.search.substring(1);
  var vars = query.split("&");

  for (var i = 0; i < vars.length; i++) {
    var pair = vars[i].split("=");

    if (pair[0] === variable) {
      return decodeURIComponent(pair[1].replace(/\+/g, "%20"));
    }
  }
}

var searchTerm = getQueryVariable("q");
if (searchTerm) {
  lunr_search(searchTerm);
}
