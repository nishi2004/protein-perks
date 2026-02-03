document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("checkout-form");
    const payBtn = document.getElementById("pay-button");

    form.addEventListener("submit", async function (e) {

        e.preventDefault();

        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }

        payBtn.disabled = true;
        payBtn.innerText = "Processing...";

        const formData = new FormData(form);

        try {

            // 1️⃣ Create Razorpay Order
            const res = await fetch("/checkout/create-order", {
                method: "POST",
                body: formData
            });

            const data = await res.json();

            if (!data.success) {
                alert("Failed to create payment order!");
                payBtn.disabled = false;
                payBtn.innerText = `Pay ₹${totalAmount}`;
                return;
            }


            // 2️⃣ Razorpay Options
            const options = {

                key: razorpayKeyId,
                amount: data.amount,
                currency: "INR",
                name: "Protein Perks",
                description: "Order Payment",
                order_id: data.order_id,

                prefill: {
                    name: formData.get("name"),
                    email: formData.get("email"),
                    contact: formData.get("phone")
                },

                handler: async function (response) {

                    // 3️⃣ Verify Payment
                    const verifyData = new FormData();

                    verifyData.append("razorpay_order_id", response.razorpay_order_id);
                    verifyData.append("razorpay_payment_id", response.razorpay_payment_id);
                    verifyData.append("razorpay_signature", response.razorpay_signature);

                    const verifyRes = await fetch("/payment/verify", {
                        method: "POST",
                        body: verifyData
                    });

                    const verifyResult = await verifyRes.json();

                    if (!verifyResult.success) {
                        alert("Payment verification failed!");
                        window.location.href = "/payment/failure";
                        return;
                    }


                    // 4️⃣ Save Order in DB ✅
                    const saveRes = await fetch("/checkout/payment-success", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify(response)
                    });

                    const saveResult = await saveRes.json();

                    if (saveResult.success) {
                        window.location.href = "/order-success";
                    } else {
                        alert("Order saving failed!");
                        window.location.href = "/payment/failure";
                    }

                },

                theme: {
                    color: "#4F46E5"
                }
            };


            // 5️⃣ Open Razorpay
            const rzp = new Razorpay(options);
            rzp.open();


        } catch (err) {

            console.error(err);
            alert("Something went wrong!");
            payBtn.disabled = false;
            payBtn.innerText = `Pay ₹${totalAmount}`;

        }

    });

});
