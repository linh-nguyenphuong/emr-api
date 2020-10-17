class ErrorTemplate:
        ADMIN_REQUIRED = dict(
            message='Yêu cầu đăng nhập bằng tài khoản quản trị.'
        )

        USER_REQUIRED = dict(
            message='Yêu cầu đăng nhập.'
        )

        EMAIL_REQUIRED = dict(
            message='Vui lòng nhập địa chỉ email.'
        )

        EMAIL_ALREADY_EXISTED = dict(
            message='Địa chỉ email này đã được sử dụng.'
        )

        CANNOT_UPDATE_EMAIL = dict(
            message='Không thể cập nhật địa chỉ email.'
        )

        PHONE_REQUIRED = dict(
            message='Vui lòng nhập số điện thoại.'
        )

        PHONE_ALREADY_EXISTED = dict(
            message='Số điện thoại này đã được sử dụng.'
        )

        INCORRECT_EMAIL_OR_PHONE = dict(
            message='Không tìm thấy tài khoản sử dụng email/số điện thoại này.'
        )

        INCORRECT_PASSWORD = dict(
            message='Mật khẩu không chính xác.'
        )

        USER_NOT_EXIST = dict(
            message='Mã người dùng không tồn tại.'
        )

        PASSWORDS_NOT_MATCH = dict(
            message='Mật khẩu không trùng khớp.'
        )

        EXPIRED_LINK = dict(
            message='Đường dẫn dùng để xác thực này đã hết hạn.'
        )

        VERIFIED_EMAIL_REQUIRED = dict(
            message='Vui lòng xác thực địa chỉ email này để thực hiện đăng nhập.'
        )

        VERIFIED_PHONE_REQUIRED = dict(
            message='Vui lòng xác thực số điện thoại này để thực hiện đăng nhập.'
        )

        VERIFIED_EMAIL = dict(
            message='Địa chỉ email này đã được xác minh.'
        )

        EMAIL_NOT_EXIST = dict(
            message='Địa chỉ email này chưa tồn tại.'
        )

        INVALID_RESET_PASSWORD_LINK = dict(
            message='Đường dẫn không hợp lệ.'
        )

        FIELDS_REQUIRED = dict(
            message='Vui lòng truyền đầy đủ các trường.'
        )

        NOT_BLOCK_OLDER_ADMIN = dict(
            message='Không thể khóa tài khoản admin được tạo ra trước tài khoản hiện tại.'
        )

        CANNOT_UPLOAD_IMAGE = dict(
            message='Không thể tải ảnh lên, xin vui lòng kiểm tra lại.'
        )

        IMAGE_REQUIRED = dict(
            message='Vui lòng tải lên ít nhất 1 ảnh.'
        )

        IMAGE_NOT_EXIST = dict(
            message='Mã hình ảnh không tồn tại.'
        )

        PROFILE_NOT_FOUND = dict(
            message='Không tìm thấy trang thông tin cá nhân.'
        )

        INVALID_IMAGE = dict(
            message='Định dạng hình ảnh không được cho phép.'
        )

        ROLE_NOT_EXIST = dict(
            message='Mã chức danh không tồn tại.'
        )

        DRUG_CATEGORY_NOT_EXIST = dict(
            message='Mã loại thuốc không tồn tại.'
        )