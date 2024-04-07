odoo.define("gech_property_management.DialogComponent", function () {
    "use strict";

    const {Component} = owl;
    const {useService} = owl.hooks;

    class DialogComponent extends Component {
        constructor() {
            super(...arguments);
            this.notification = useService("notification");
        }

        mounted() {
            this.notification.add("You need to save the contract first.", {
                title: "Save Contract",
                sticky: true,
                // Buttons: [
                //     {
                //         name: 'Save',
                //         primary: true,
                //         onClick: () => {
                //             // Call the save method on the current record
                //             this.env.model.call('save_contract', []);
                //             this.notification.removeAll();
                //         },
                //     },
                //     {
                //         name: 'Cancel',
                //         onClick: () => {
                //             this.notification.removeAll();
                //         },
                //     },
                // ],
            });
        }
    }

    return DialogComponent;
});
