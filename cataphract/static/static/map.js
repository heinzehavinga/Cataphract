// Get the CSRF token from the cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

var selectedType = 0;
var selectedTile = "";
const coordToPos = (ox, oy) => {
    size = 72
    x = ox * (size*.75)
    y = oy * size
    if (ox%2 == 1)
        y += size/2
    return [x, y]
}

var mapEl, regionEl
var mapUrl = ""
const updateHex = async (id, type, tile) => {
    console.log("updateHex")
    fetch("/cataphract/map/1", {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-CSRFToken": csrftoken},
        body: JSON.stringify({"hex_id": id, "type": type, "tile": tile }),
    })
    .then(response => {
        if (response.status == 200) {
            // console.log("done. need to refresh image")
            // mapEl.setAttribute("src", mapUrl + "?t=" + new Date().getTime())
        }
        return response.json()
    })
    .then(json => {
        console.log(">>>")
        console.log(json)
        mapEl.setAttribute("src", `/media/${json.data['new_src']}`)
        regionEl.setAttribute("src", `/media/${json.data['new_region_src']}`)
    })
    .catch(error => console.error('Error:', error));
}
document.addEventListener("DOMContentLoaded", (_) => {
    mapEl = document.getElementById("map-image")
    regionEl = document.getElementById("region-overlay")
    mapUrl = mapEl.getAttribute("src")
    const allTiles = document.querySelectorAll(".tile")
    const cursorEl = document.getElementById("cursor")
    document.querySelectorAll("area").forEach( (el) => {
        el.addEventListener("mouseenter", (e) => {
            pos = coordToPos(el.dataset.x, el.dataset.y)
            cursorEl.style.left = `${pos[0]}px`
            cursorEl.style.top = `${pos[1]}px`
        })
        el.addEventListener("click", (e) => {
            e.preventDefault()
            console.log("clicky!", e.target.id, selectedType)
            updateHex(e.target.id, selectedType, selectedTile)
        })
    })
    document.querySelectorAll("img.tile").forEach( (el) => {
        el.addEventListener("click", (e) => {
            allTiles.forEach((el) => el.classList.remove("selected") )
            el.classList.add("selected")
            selectedType = el.dataset.type
            selectedTile = el.dataset.tile
            console.log("selected", selectedType)
        })
    })
})