/**
 * This function checks the selected type and rearrange the form in appropriate form.
 */
function use_type_change()
{
    let set_hidden_for_all = (all,value) =>
    {
        for(let i = 0; i < all.length; i++)
        {
            all[i].hidden = value;
        }
    };
    let reset = () =>
    {
        let all = document.getElementsByClassName("js_extra");
        set_hidden_for_all(all,true);
    };
    let type_selector = document.getElementById("js_type_select");
    let selected_value = type_selector.options[type_selector.selectedIndex].value;
    if(selected_value === "education")
    {
        reset();
        let forms = document.getElementsByClassName("js_edu_extra");
        set_hidden_for_all(forms,false);
    }
    else if (selected_value === "research")
    {
        reset();
        let forms = document.getElementsByClassName("js_res_extra");
        set_hidden_for_all(forms,false);
    }
    else
    {
        reset();
    }
}


function check_inputs()
{
    let form_inputs = document.getElementsByClassName("js_fi");
    let use_type_selector = document.getElementById("js_type_select");
    let use_type = use_type_selector.options[use_type_selector.selectedIndex].value;
    let is_item_missing = false;
    for(let i = 0; i <form_inputs.length; i++)
    {
        if(form_inputs[i].value === "")
        {
            if(form_inputs[i].dataset.req === "true")
            {
                form_inputs[i].style.borderColor = "#ff0013";
                is_item_missing = true;
            }
            if(use_type === "research" && form_inputs[i].dataset.req === "cond")
            {
                form_inputs[i].style.borderColor = "#ff0013";
                is_item_missing = true;
            }

        }
        else
        {
            form_inputs[i].style.borderColor = null;
        }
    }

    let notifier = document.getElementById("required");
    if(is_item_missing)
    {
        notifier.hidden = false;
        notifier.innerText = "Fill the required field!";
    }
    else
    {
        notifier.hidden = true;
    }

}
