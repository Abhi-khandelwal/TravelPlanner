let destinationCount = 1;

function appendInput() {
    let parent = document.createElement("div");
    parent.id = "destination" + destinationCount;
    parent.classList += "form-group";
    let row = document.createElement("div");
    row.classList += "row";

    let labelDiv = document.createElement("div");
    labelDiv.classList += "col-4";
    let label = document.createElement("label");
    label.for = "destination-" + destinationCount;
    label.appendChild(document.createTextNode("Destination:"));
    labelDiv.appendChild(label);
    row.appendChild(labelDiv);

    let nameDiv = document.createElement("div");
    nameDiv.classList += "col-4";
    let nameInput = document.createElement("input");
    nameInput.classList += "form-control";
    nameInput.name = "destinations[]";
    nameInput.id = "destination-" + destinationCount;
    nameDiv.appendChild(nameInput);
    row.appendChild(nameDiv);

    let numberDiv = document.createElement("div");
    numberDiv.classList += "col-2";
    let numberInput = document.createElement("input");
    numberInput.classList += "form-control";
    numberInput.name = "destination-durations[]";
    numberInput.placeholder = "DUR";
    numberInput.type = "number";
    numberDiv.appendChild(numberInput);
    row.appendChild(numberDiv);

    let buttonDiv = document.createElement("div");
    buttonDiv.classList += "col-2";
    let button = document.createElement("button");
    button.classList += "btn btn-outline-danger";
    button.appendChild(document.createTextNode("Delete"));
    button.addEventListener("click", function () {
        parent.remove();
    });
    buttonDiv.appendChild(button);
    row.appendChild(buttonDiv);

    parent.appendChild(row);
    document.getElementById("destination-container").appendChild(parent);
    ++destinationCount;
}


(function () {
    appendInput();
    document.getElementById("addDestination").addEventListener("click", function (){
        appendInput();
    });
    var elements =  Array.from(document.getElementsByClassName("tab"));
    console.log(elements);
		elements.forEach(function(element) {
    	element.addEventListener("click", function(){
    		elements.forEach(function(elem) {
    			elem.classList.remove("active");
    		})
    		element.classList.add("active");

    		Array.from(document.getElementsByClassName("result-container")).forEach(function(element){
    			element.classList.add("hidden");
    		});
    		document.getElementById("addTrip-result").classList.add("hidden");
    		document.getElementById(element.id+"-result").classList.remove("hidden");
    	})
	});
})();
