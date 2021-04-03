function removeSelected() {
    let playerFighter = document.getElementById('player_select');
    let cpuFighter = document.getElementById('cpu_select')
    for (i = 0; i < playerFighter.length; i++) {
        if (playerFighter[i].selectedIndex) {
            cpuFighter.remove[i]
        }
    }
    return cpuFighter
}



// Enumerate all lists
var Lists = [
    document.getElementById("player_select"),
    document.getElementById("user_select"),
],
    nbLists = Lists.length;


// Binds change events to each list
for (var iList = 0; iList < nbLists; iList++) {
    Lists[iList].onchange = RemoveItems(iList);
}


function RemoveItems(iList) {
    return function () {
        var value = [];

        // Add the selected items of all previous lists including the one changed
        for (var jList = 0; jList <= iList; jList++) value.push(Lists[jList].options[Lists[jList].selectedIndex].text);


        // Hide in all succeeding lists these items
        for (var kList = iList + 1; kList < nbLists; kList++)
            HideItems(kList, value);
    }
}


// Hide items selected in previous list in next list
function HideItems(iList, value) {
    var nbOptions = Lists[iList].options.length,
        nbValues = value.length,
        found;

    if (nbValues === 0) return;

    for (var iOption = 0; iOption < nbOptions; iOption++) {
        // Find if this element is present in the previous list
        found = false;
        for (var iValue = 0; iValue < nbValues; iValue++) {
            if (Lists[iList].options[iOption].text === value[iValue]) {
                found = true;
                break;
            }
        }

        // If found, we hide it
        if (found) {
            Lists[iList].options[iOption].style.display = "none";
            Lists[iList].options[iOption].selected = "";
        }
        // else we un-hide it (in case it was previously hidden)
        else
            Lists[iList].options[iOption].style.display = "";
    }
}
