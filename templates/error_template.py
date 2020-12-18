class ErrorTemplate:
        ADMIN_REQUIRED = dict(
            message='Yêu cầu đăng nhập bằng tài khoản quản trị.'
        )

        USER_REQUIRED = dict(
            message='Yêu cầu đăng nhập bằng tài khoản người dùng.'
        )

        PHYSICIAN_REQUIRED = dict(
            message='Yêu cầu đăng nhập bằng tài khoản bác sĩ.'
        )

        ADMIN_OR_PHYSICIAN_REQUIRED = dict(
            message='Yêu cầu đăng nhập bằng tài khoản quản trị hoặc bác sĩ.'
        )

        PHYSICIAN_OR_RECEPTION_REQUIRED = dict(
            message='Yêu cầu đăng nhập bằng tài khoản bác sĩ hoặc tiếp tân.'
        )

        EMAIL_REQUIRED = dict(
            message='Vui lòng nhập địa chỉ email.'
        )

        EMAIL_ALREADY_EXISTED = dict(
            message='Địa chỉ email này đã được sử dụng.'
        )

        CANNOT_UPDATE_EMAIL = dict(
            message='Không cho phép cập nhật địa chỉ email.'
        )

        CANNOT_UPDATE_PHONE = dict(
            message='Không cho phép cập nhật địa chỉ email.'
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
            message='Hình ảnh không tồn tại.'
        )

        PROFILE_NOT_FOUND = dict(
            message='Không tìm thấy trang thông tin cá nhân.'
        )

        INVALID_IMAGE = dict(
            message='Định dạng hình ảnh không được cho phép.'
        )

        ROLE_NOT_EXIST = dict(
            message='Chức danh không tồn tại.'
        )

        DRUG_CATEGORY_NOT_EXIST = dict(
            message='Loại thuốc không tồn tại.'
        )

        DRUG_UNIT_NOT_EXIST = dict(
            message='Đơn vị thuốc không tồn tại.'
        )

        DRUG_NOT_EXIST = dict(
            message='Thuốc không tồn tại.'
        )

        DRUG_INSTRUCTION_NOT_EXIST = dict(
            message='Hướng dẫn không tồn tại.'
        )

        DRUG_DOSAGE_FORM_NOT_EXIST = dict(
            message='Dạng bào chế không tồn tại.'
        )

        DRUG_ROUTE_NOT_EXIST = dict(
            message='Đường dùng không tồn tại.'
        )

        DISEASE_CATEGORY_NOT_EXIST = dict(
            message='Loại bệnh không tồn tại.'
        )

        DISEASE_NOT_EXIST = dict(
            message='Bệnh không tồn tại.'
        )

        SERVICE_NOT_EXIST = dict(
            message='Dịch vụ không tồn tại.'
        )

        WORKING_NOT_EXIST = dict(
            message='Giờ làm việc không tồn tại.'
        )

        SETTING_NOT_EXIST = dict(
            message='Tùy chỉnh cài đặt không tồn tại.'
        )

        ROOM_NOT_EXIST = dict(
            message='Phòng không tồn tại.'
        )

        PATIENT_REQUIRED = dict(
            message='Yêu cầu nhập mã bệnh nhân.'
        )

        PATIENT_NOT_EXIST = dict(
            message='Bệnh nhân không đúng.'
        )

        PHYSICIAN_NOT_EXIST = dict(
            message='Bác sĩ không đúng.'
        )

        APPOINTMENT_NOT_EXIST = dict(
            message='Cuộc hẹn không tồn tại.'
        )

        APPOINTMENT_NOT_UPDATE = dict(
            message='Cuộc hẹn đã được chấp nhận, không thể update.'
        )

        DELETE_APPOINTMENT_NOT_ALLOW = dict(
            message='Xóa cuộc hẹn chỉ được thực hiện bởi người khởi tạo nó.'
        )

        CANNOT_ACCEPT_OR_REJECT_APPOINTMENT = dict(
            message='Tài khoản này không có quyền xét duyệt cuộc hẹn.'
        )
        
        VISIT_NOT_EXIST = dict(
            message='Lần đến khám không tồn tại.'
        )

        EMR_NOT_EXIST = dict(
            message='Bệnh án không tồn tại.'
        )

        EMR_NOT_UPDATE = dict(
            message='Bệnh án đã được đóng, không thể cập nhật hay xóa.'
        )

        DISEASE_EXISTED_IN_EMR = dict(
            message='Bệnh này đã được thêm vào bệnh án.'
        )

        DISEASE_NOT_EXIST_IN_EMR = dict(
            message='Bệnh này chưa được thêm vào bệnh án.'
        )

        DRUG_EXISTED_IN_EMR = dict(
            message='Thuốc này đã được thêm vào bệnh án.'
        )

        DRUG_NOT_EXIST_IN_EMR = dict(
            message='Thuốc này chưa được thêm vào bệnh án.'
        )

        SERVICE_EXISTED_IN_EMR = dict(
            message='Dịch vụ này đã được thêm vào bệnh án.'
        )

        SERVICE_NOT_EXIST_IN_EMR = dict(
            message='Dịch vụ này chưa được thêm vào bệnh án.'
        )

        CANNOT_ACCESS_EMR = dict(
            message='Không thể xem bệnh án này'
        )

        SERVICE_ALREADY_EXISTED = dict(
            message='Tên dịch vụ đã tồn tại.'
        )

        DISEASE_CODE_ALREADY_EXISTED = dict(
            message='Mã bệnh đã tồn tại.'
        )

        DRUG_CODE_ALREADY_EXISTED = dict(
            message='Mã thuốc đã tồn tại.'
        )
