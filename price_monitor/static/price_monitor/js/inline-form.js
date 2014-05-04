$(document).ready(function() {
    var formCounterInput = $('#id_form-TOTAL_FORMS');
    // resetting form counter to rendered form count as Firefox will keep value after refresh
    formCounterInput.val($('form.form-inline .form-line:not(#empty-line)').length);

    /**
     * Adds a new line to inline form
     */
    function addLine() {
        // clone the new line and remove it's id
        var newLine = $('#empty-line').clone().removeAttr('id');

        // replace __prefix__ in form elements of new line
        newLine.find('input, select').each(function(index, element) {
            // length - 1 is used here because empty line is also counted
            $(element).attr('id', $(element).attr('id').replace('__prefix__', $('form.form-inline .form-line').length - 1));
        });

        // add it
        $('form.form-inline .form-line:last').after(newLine);

        // remove hidden class from remove buttons
        $('form.form-inline .form-line .form-remove-button').removeClass('hidden');

        // set form count in management form
        formCounterInput.val(parseInt(formCounterInput.val()) + 1);
    }

    /**
     * Removes line from form
     * @param line: the line to remove
     */
    function removeLine(line) {
        // remove the line
        line.remove();

        // set form count
        formCounterInput.val(parseInt(formCounterInput.val()) - 1);

        // if there is only one line, hide remove button
        if ($('form.form-inline .form-line:not(#empty-line)').length <= 1) {
            $('form.form-inline .form-line .form-remove-button').addClass('hidden');
        }
    }

    // attach handler to add button
    $('#form-add-button').click(function() {
        addLine();
    });

    // add handler to present and future remove buttons
    $('form.form-inline').on('click', ' .form-line .form-remove-button', function(event) {
        removeLine($(event.target).parents('.form-line'));
    });
});
