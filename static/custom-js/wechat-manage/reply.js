/**
 * Created by machao on 2016/12/19.
 */


        $(document).ready(
            function () {

                var type_select = $('[name=content_type]');
                var text_area = $('[name = content]').parent().parent(), file_upload = $('[name=file]').parent().parent();

                function handle_type_select() {
                    var value = parseInt($(this).val());
                    text_area.find('[name=content]').val(null);
                    file_upload.find('[name=file]').val(null);
                    text_area.hide();
                    file_upload.hide();
                    switch (value) {
                        case 1:
                            text_area.show();
                            break;
                        case 2:
                        case 3:
                        case 5:
                            file_upload.show();
                            break;
                    }

                }

                handle_type_select.call(type_select);

                type_select.change(handle_type_select)

            }
        )
