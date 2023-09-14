const $searchBar = $('#ing');
const $suggestions = $('.suggestions ul');
const $ingList = $('#ing-list')

const fruit = ['Apple', 'Apricot', 'Avocado 🥑', 'Banana', 'Bilberry', 'Blackberry', 'Blackcurrant', 'Blueberry', 'Boysenberry', 'Currant', 'Cherry', 'Coconut', 'Cranberry', 'Cucumber', 'Custard apple', 'Damson', 'Date', 'Dragonfruit', 'Durian', 'Elderberry', 'Feijoa', 'Fig', 'Gooseberry', 'Grape', 'Raisin', 'Grapefruit', 'Guava', 'Honeyberry', 'Huckleberry', 'Jabuticaba', 'Jackfruit', 'Jambul', 'Juniper berry', 'Kiwifruit', 'Kumquat', 'Lemon', 'Lime', 'Loquat', 'Longan', 'Lychee', 'Mango', 'Mangosteen', 'Marionberry', 'Melon', 'Cantaloupe', 'Honeydew', 'Watermelon', 'Miracle fruit', 'Mulberry', 'Nectarine', 'Nance', 'Olive', 'Orange', 'Clementine', 'Mandarine', 'Tangerine', 'Papaya', 'Passionfruit', 'Peach', 'Pear', 'Persimmon', 'Plantain', 'Plum', 'Pineapple', 'Pomegranate', 'Pomelo', 'Quince', 'Raspberry', 'Salmonberry', 'Rambutan', 'Redcurrant', 'Salak', 'Satsuma', 'Soursop', 'Star fruit', 'Strawberry', 'Tamarillo', 'Tamarind', 'Yuzu'];

async function search(str) {
	const res = await axios.get(`http://localhost:5000/ingredient/search/${str}`)
	console.log(res)
	return res.data;
}

async function searchHandler(e) {
	// TODO
	e.preventDefault();
	cleanUp();
	const inputVal = $searchBar.val();
	if(inputVal !== ""){
		const resultArr = await search(inputVal);
		showSuggestions(resultArr);
	};

}

function showSuggestions(results) {
	// TODO
	results.forEach(element => {
		appendSuggestion(element)
	});
}



async function useSuggestion(e) {
	// TODO
	const usedSugg = e.target.innerText;
	$searchBar.val('')
	p_id = $searchBar.data('pantry-id')
	resp = await axios.get(`http://localhost:5000/pantry/${p_id}/ingredient/${usedSugg}`)
	cleanUp();
}

function cleanUp(){
	$suggestions.empty()
}

function appendSuggestion(str){
	const $newSuggestion = $('<li>'+str+'</li>');
	$suggestions.append($newSuggestion);
}

$searchBar.on('keyup', searchHandler);
$suggestions.on('click', useSuggestion);
$
