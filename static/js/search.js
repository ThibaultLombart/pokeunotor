function getSuggestions() {
    var input = document.getElementById('searchInput').value;

    if (input.trim() === '') {
        clearSuggestions();
        return;
    }

    // Requête Ajax pour demander la liste a la méthode filter_and_sort_pokemon du fichier extractData.py
    $.ajax({
        type: 'GET',
        url: '/search',
        data: {'term': input},
        success: function (data) {
            displaySuggestions(data);
        }
    });
}

function displaySuggestions(suggestions) {
    var list = document.getElementById('suggestionsList');
    list.innerHTML = '';

    // Afficher les suggestions dans la liste
    suggestions.forEach(function (pokemon) {
        var li = document.createElement('li');
        var img = document.createElement('img');

        img.src = pokemon.url;

        li.appendChild(img);

        li.appendChild(document.createTextNode(pokemon.name));

        var link = document.createElement('a');
        link.appendChild(li);

        link.addEventListener('click', function() {
            document.getElementById('searchInput').value = pokemon.name;
        });

        list.appendChild(link);
    });
}


function clearSuggestions() {
    var list = document.getElementById('suggestionsList');
    list.innerHTML = '';
}


// Evenement écriture.
document.getElementById('searchInput').addEventListener('input', getSuggestions);