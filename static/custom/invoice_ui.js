    var counter = 1;
    var limit = 3;

    function addLine(divName){
        // Testing only really
         if (counter == limit)  {
              alert("You have reached the limit of adding " + counter + " lines");
         }
         else {
             counter += 1;
             // Container
             var newLine = document.createElement("div");
             newLine.setAttribute("class", "row");
             newLine.setAttribute("line", counter);
             
             // Parent LEFT
             var col_0 = document.createElement("div");
             col_0.setAttribute("class", "col-md-9 mb-3");
             
             // Child LEFT
             var prodInput = document.createElement("input");
             prodInput.setAttribute("class", "form-control");
             prodInput.setAttribute("id", "product");
             prodInput.setAttribute("required", "");
             prodInput.setAttribute("type", "text");
             
             // Parent RIGHT
             var col_1 = document.createElement("div");
             col_1.setAttribute("class", "col-md-3 mb-3");
             
             // Child RIGHT
             var qntyInput = document.createElement("input");
             qntyInput.setAttribute("class", "form-control");
             qntyInput.setAttribute("id", "qty");
             qntyInput.setAttribute("required", "");
             qntyInput.setAttribute("type", "number");
             
             // Build new item line
             col_0.appendChild(prodInput);
             col_1.appendChild(qntyInput);
             newLine.appendChild(col_0);
             newLine.appendChild(col_1);
             
             
             //newLine.innerHTML = "Entry " + (counter + 1) + " <br><input type='text' name='myInputs[]'>";
             document.getElementById(divName).appendChild(newLine);
         }
    }