// General scraper for ceoddata.com/stocklist/ stock ticker lists

const filename = "tsx_"
const querySelector = 'a[href^="/stockquote/TSX"]'

function scrapeFrom(htmlCollection) {
    let result = Array.from(htmlCollection)
        .map((el) => el.innerText)
        .filter((txt) => txt && !txt.includes('%') && !txt.includes('—'))
        .reduce((acc, cur) => acc + '\n' + cur, '')

    result = result.trim()

    download(filename + result[0].toLowerCase() + '.txt', result);
}


function download(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}

scrapeFrom(document.querySelectorAll(querySelector))

// then set the next url scrape
location.href = "ceoddata.com/stocklist/TSX/B.htm"
