function create_folder() {
    /* This is how to wait for jQuery to load. */
    $(document).ready(function() {
        /* get form object from DOM using jQuery, search by id. */
        form = $('#create_folder');
        /* get a directory name from the user, prompt a form. */
        var dir_name = prompt("New directory name", "");
        if (dir_name && form) {
            /* get the hidden input from the form, and override his
             * value with the folder name received from user.
             */
            $(form).find('#hidden_directory_name').val(dir_name);
            /* Now that the folder name has been set, we can POST to
             * the server, requesting the folder to be created.
             */
            form.submit();
        }
    });
}
