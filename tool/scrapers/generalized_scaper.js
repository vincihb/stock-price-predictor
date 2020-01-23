

function scrapeFrom(htmlCollection) {
    const result = Array.from(htmlCollection)
        .map((el) => el.innerText)
        .filter((txt) => txt && !txt.includes('%') && !txt.includes('—'))
        .reduce((acc, cur) => acc + '\n' + cur, '')

    download('result.txt', result);
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