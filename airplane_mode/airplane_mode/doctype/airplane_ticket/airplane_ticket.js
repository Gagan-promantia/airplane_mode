// Copyright (c) 2025, airplane mode and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Airplane Ticket", {
// 	refresh(frm) 
// 	},
// });
frappe.ui.form.on('Airplane Ticket',{
    refresh(frm){
        frm.add_custom_button('Assign Seat',()=>{
            let d =new frappe.ui.Dialog({
                title:'Assign Seat',
                fields:[
                    {
                    label:'Seat NUmber',
                    fieldname:'seat_number',
                    fieldtype:'Data',
                    reqd:1,
                    description:'Enter seat (eg. 12A, 21B,3C)'
                    }
                ],
                primary_action_label:'Assign',
                primary_action(values){
                    frm.set_value('seat',values.seat_number);
                    //frm.save();
                    d.hide();
                    // frappe.call({
                    //     method:"airplane_mode.airplane_mode.doctype.airplane_ticket.airplane_ticket.validate_and_assign_seat",
                    //     args:{
                    //         ticket_name:frm.doc.name,
                    //         flight:frm.doc.flight,
                    //         seat:values.seat_number
                    //     },
                    //     callback:function(r){
                    //         if(!r.exc){
                    //             frm.set_value('seat',values.seat_number);
                    //             d.hide();
                    //         }
                    //     }
                    // });

                }
            });
            d.show();
        },'Actions');
    }
});
