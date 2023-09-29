const $searchBar = $('#ing');
const $suggestions = $('.suggestions');
const $ingList = $('#ing-list')
const baseURL = 'https://virtual-pantry-elvir.onrender.com'
const fruit = ['Apple', 'Apricot', 'Avocado 🥑', 'Banana', 'Bilberry', 'Blackberry', 'Blackcurrant', 'Blueberry', 'Boysenberry', 'Currant', 'Cherry', 'Coconut', 'Cranberry', 'Cucumber', 'Custard apple', 'Damson', 'Date', 'Dragonfruit', 'Durian', 'Elderberry', 'Feijoa', 'Fig', 'Gooseberry', 'Grape', 'Raisin', 'Grapefruit', 'Guava', 'Honeyberry', 'Huckleberry', 'Jabuticaba', 'Jackfruit', 'Jambul', 'Juniper berry', 'Kiwifruit', 'Kumquat', 'Lemon', 'Lime', 'Loquat', 'Longan', 'Lychee', 'Mango', 'Mangosteen', 'Marionberry', 'Melon', 'Cantaloupe', 'Honeydew', 'Watermelon', 'Miracle fruit', 'Mulberry', 'Nectarine', 'Nance', 'Olive', 'Orange', 'Clementine', 'Mandarine', 'Tangerine', 'Papaya', 'Passionfruit', 'Peach', 'Pear', 'Persimmon', 'Plantain', 'Plum', 'Pineapple', 'Pomegranate', 'Pomelo', 'Quince', 'Raspberry', 'Salmonberry', 'Rambutan', 'Redcurrant', 'Salak', 'Satsuma', 'Soursop', 'Star fruit', 'Strawberry', 'Tamarillo', 'Tamarind', 'Yuzu'];

async function search(str) {
	const res = await axios.get(`${baseURL}/ingredient/search/${str}`)
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
	resp = await axios.get(`${baseURL}/pantry/${p_id}/ingredient/${usedSugg}`)
	cleanUp();
	updateIngredientsList()
}

function cleanUp(){
	$suggestions.empty()
}

function appendSuggestion(str){
	const $newSuggestion = $('<a href="#" class="list-group-item list-group-item-action">'+str+'</a>');
	$suggestions.append($newSuggestion);
}

async function updateIngredientsList(){
	p_id = $searchBar.data('pantry-id')
	resp = await axios.get(`${baseURL}/pantry/${p_id}/ingredient`)
	$ingList.empty()
	console.log(resp)
	for(let x in resp.data){
		console.log(typeof resp.data[x])
		ing= resp.data[x]
		$ingredient = $(`
						<div class="rounded border border-primary px-3 py-2 my-2 mx-1">
            				<li>
                				<form action="/pantry/${p_id}/ingredient/${ing['id']}/remove" method="post">
                    				<div style="display: flex; justify-content: space-between; align-items: center;">
                        				<h5><a href="/recipe/search/${ing['name']}" class="link-opacity-50-hover p-6">${ing['name']}</a></h5>
                        				<span class="m-2"></span>
                        				<button class="btn btn-sm btn-danger" type="submit">&#10005;</button>
                    				</div>
                				</form>
            				</li>
        				</div>`)
		
		$ingList.append($ingredient)				
	}
}

$searchBar.on('keyup', searchHandler);
$suggestions.on('click', useSuggestion);

