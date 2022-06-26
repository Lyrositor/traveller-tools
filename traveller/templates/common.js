const HEX_INFO = {{hexes_by_coords|tojson}}

export const TRADE_GOODS = {{trade_goods|tojson}}

export function getHexInfo(coords) {
    if (HEX_INFO.hasOwnProperty(coords)) {
        return HEX_INFO[coords]
    }
    return null
}

export function selectText(node) {
    if (document.body.createTextRange) {
        const range = document.body.createTextRange()
        range.moveToElementText(node)
        range.select()
    } else if (window.getSelection) {
        const selection = window.getSelection()
        const range = document.createRange()
        range.selectNodeContents(node)
        selection.removeAllRanges()
        selection.addRange(range)
    } else {
        console.warn("Could not select text in node: Unsupported browser.")
    }
}

export function dm(value) {
    return (value >= 0) ? '+' + value.toString() : value.toString()
}
