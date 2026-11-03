function parseSymbols(raw) {
  try {
    var data = JSON.parse(String(raw || ""))
    return Array.isArray(data) ? data : []
  } catch (e) {
    return []
  }
}

// Lower is better: exact word 0, word prefix 1, substring 2, no match -1.
// One-letter words only match exactly, so "e" means the letter and not every word starting with e.
function tokenScore(word, tokens) {
  var best = -1
  var exactOnly = word.length === 1
  for (var i = 0; i < tokens.length; i++) {
    var token = tokens[i]
    var score = token === word ? 0 : exactOnly ? -1 : token.indexOf(word) === 0 ? 1 : word.length >= 3 && token.indexOf(word) >= 0 ? 2 : -1
    if (score >= 0 && (best < 0 || score < best)) best = score
  }
  return best
}

function itemScore(item, words, rawQuery) {
  if (item.e === rawQuery) return 0
  var tokens = String(item.k || "").split(" ")
  var total = 0
  for (var i = 0; i < words.length; i++) {
    var score = tokenScore(words[i], tokens)
    if (score < 0) return -1
    total += score
  }
  return total
}

// A single typed capital ("E") narrows to capital letters.
function wantsCapital(rawQuery) {
  return /^[A-Z]$/.test(rawQuery)
}

function filterSymbols(symbols, query, limit) {
  var values = Array.isArray(symbols) ? symbols : []
  var rawQuery = String(query || "").trim()
  var words = rawQuery.toLowerCase().split(/\s+/).filter(function(w) { return w.length > 0 })
  var max = Math.max(0, Number(limit) || 1000)
  if (words.length === 0) return values.slice(0, max)

  var capitalOnly = wantsCapital(rawQuery)
  var scored = []
  for (var i = 0; i < values.length; i++) {
    var item = values[i]
    if (!item || !item.e) continue
    if (capitalOnly && item.e === item.e.toLowerCase()) continue
    var score = itemScore(item, words, rawQuery)
    if (score >= 0) scored.push({ item: item, score: score, order: i })
  }

  scored.sort(function(a, b) { return a.score - b.score || a.order - b.order })
  return scored.slice(0, max).map(function(s) { return s.item })
}

if (typeof module !== "undefined") {
  module.exports = { parseSymbols: parseSymbols, filterSymbols: filterSymbols }
}
