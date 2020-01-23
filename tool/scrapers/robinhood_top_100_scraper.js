// from https://robinhood.com/collections/100-most-popular
// returns a \n seperated list of the top 10 stocks on robinhood
Array.from(document.querySelectorAll('._3-Fg9lFlzey28mCJClXXxZ a.rh-hyperlink[href^="/stocks/"] span'))
    .map((el) => el.innerText)
    .filter((txt) => !txt.includes('%') && !txt.includes('—'))
    .reduce((acc, cur) => acc + '\n' + cur, '')