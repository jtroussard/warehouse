    var counter = 1;
    var limit = 10;

    function addLine(divName){
         if (counter == limit)  {
              alert("You have reached the limit of adding " + counter + " lines");
         }
         else if (document.getElementById(counter+"_product").value == "") {
              alert("Complete current line before adding another.\n\nSee Product Number field.");
         }
         else if (document.getElementById(counter+"_quantity").value == "") {
              alert("Complete current line before adding another.\n\nSee Quantity field.");
         }
         else {
             counter += 1;
             // Container
             var newLine = document.createElement("div");
             newLine.setAttribute("class", "row");
             newLine.setAttribute("line", counter);
             
             // Parent LEFT (Product)
             var col_0 = document.createElement("div");
             col_0.setAttribute("class", "col-md-9 mb-3");
             
             // Child LEFT
             var prodInput = document.createElement("input");
             prodInput.id = counter + "_product";
             prodInput.setAttribute("class", "form-control");
             prodInput.setAttribute("name", "products[]");
             prodInput.setAttribute("required", "");
             prodInput.setAttribute("type", "text");
             
             // Parent RIGHT (Quantity)
             var col_1 = document.createElement("div");
             col_1.setAttribute("class", "col-md-3 mb-3");
             
             // Child RIGHT
             var qntyInput = document.createElement("input");
             qntyInput.id = counter + "_quantity";
             qntyInput.setAttribute("class", "form-control");
             qntyInput.setAttribute("name", "qtys[]");
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