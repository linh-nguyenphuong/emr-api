class ErrorTemplate:
        ADMIN_REQUIRED = dict(
            success=False,
            message='Yêu cầu đăng nhập bằng tài khoản quản trị.'
        )

        USER_REQUIRED = dict(
            success=False,
            message='Yêu cầu đăng nhập.'
        )

        EMAIL_ALREADY_EXISTED = dict(
            success=False,
            message='Địa chỉ email này đã được sử dụng.'
        )

        INCORRECT_EMAIL = dict(
            success=False,
            message='Không tìm thấy tài khoản sử dụng email này.'
        )

        INCORRECT_PASSWORD = dict(
            success=False,
            message='Mật khẩu không chính xác.'
        )

        USER_NOT_EXIST = dict(
            success=False,
            message='Mã người dùng không tồn tại.'
        )

        PASSWORDS_NOT_MATCH = dict(
            success=False,
            message='Mật khẩu không trùng khớp.'
        )

        EXPIRED_LINK = dict(
            success=False,
            message='Đường dẫn dùng để xác thực này đã hết hạn.'
        )

        VERIFIED_EMAIL_REQUIRED = dict(
            success=False,
            message='Vui lòng xác thực địa chỉ email này để thực hiện đăng nhập.'
        )

        VERIFIED_EMAIL = dict(
            success=False,
            message='Địa chỉ email này đã được xác minh.'
        )

        EMAIL_NOT_EXIST = dict(
            success=False,
            message='Địa chỉ email này chưa tồn tại.'
        )

        INVALID_RESET_PASSWORD_LINK = dict(
            success=False,
            message='Đường dẫn không hợp lệ.'
        )

        FIELDS_REQUIRED = dict(
            success=False,
            message='Vui lòng truyền đầy đủ các trường.'
        )

        NOT_BLOCK_OLDER_ADMIN = dict(
            success=False,
            message='Không thể khóa tài khoản admin được tạo ra trước tài khoản hiện tại.'
        )

        CANNOT_UPLOAD_IMAGE = dict(
            success=False,
            message='Không thể tải ảnh lên, xin vui lòng kiểm tra lại.'
        )

        IMAGE_REQUIRED = dict(
            success=False,
            message='Vui lòng tải lên ít nhất 1 ảnh.'
        )

        IMAGE_NOT_EXIST = dict(
            success=False,
            message='Mã hình ảnh không tồn tại.'
        )

        PROFILE_NOT_FOUND = dict(
            success=False,
            message='Không tìm thấy trang thông tin cá nhân.'
        )

        INVALID_IMAGE = dict(
            success=False,
            message='Định dạng hình ảnh không được cho phép.'
        )

        ROLE_EXIST = dict(
            success=False,
            message='Role này đã tồn tại.'
        )