const paymentForm = document.getElementById('donate-btn');
const publicKey = JSON.parse(document.getElementById('public_key').textContent);
const emailInput = document.getElementById("id_email_address");
const amountInput = document.getElementById("id_amount");
const fullNameInput = document.getElementById("id_full_name");
const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']");


paymentForm.addEventListener("click", payWithPaystack, false);
function payWithPaystack(e) {
    e.preventDefault();
    const data = {
        'csrfmiddlewaretoken': csrfToken.value,
        'full_name': fullNameInput.value,
        'email_address': emailInput.value,
        'amount': amountInput.value
    };
    const saveFormUrl = window.location.href;
    let refId = saveFormToDB(data, saveFormUrl);
    let handler = PaystackPop.setup({
        key: publicKey, // 
        email: emailInput.value,
        amount: amountInput.value * 100, //* 100 so as to convert to naira
        ref: refId, // returns the ref_id in the db
        currency: 'NGN',
        onClose: function () {
            alert('Window closed.');
        },
        callback: function (response) {
            let reference = response.reference;
            //   verify transaction 
            $.ajax({
                type: 'GET',
                url: `${window.location.href}verify/${reference}`,
                success: function (response) {
                    console.log(response.data.status==="success");
                    if (response.data.status==="success"){
                        window.location = `${window.location.href}success/`;
                        return;
                    }
                    window.location = `${window.location.href}failure/`;
                }
            });
        }
    });
    handler.openIframe();
}



function saveFormToDB(data, url) {
    let refId = [];
    $.ajax({
        type: 'POST',
        async: false,
        url: url,
        data: data,
        success: function (response) {
            console.log(response);
            refId.push(response.ref_id);
            
        }
    });
    console.log(refId[0]);
    return refId[0];
}