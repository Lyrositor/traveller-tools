import {createApp} from 'https://unpkg.com/vue@3/dist/vue.esm-browser.prod.js'

function getHexInfoBox(hex) {
    return $("#hex-" + $(hex).text())
}

createApp({
    mounted() {
        $('svg > g > g[clip-path="url(#did2)"] > g > text').hover(function (e) {
            const hexInfo = getHexInfoBox(this)
            hexInfo.show()
            hexInfo.css({left: e.clientX + "px", top: e.clientY - 10 - hexInfo.height() + "px"})
        }, function () {
            const hexInfo = getHexInfoBox(this)
            hexInfo.hide()
        })
    },
}).mount('#app')
