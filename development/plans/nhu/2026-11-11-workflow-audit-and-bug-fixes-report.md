# Báo cáo Rà soát & Khắc phục Lỗi Quy trình Nghiệp vụ Toàn Hệ thống (FE-01 đến FE-07)

**Người thực hiện / Tổng hợp:** Trương Thái Như (kèm rà soát mã nguồn Backend)
**Ngày hoàn thành:** 11/11/2026
**Phạm vi:** Rà soát và khắc phục các lỗi sai lệch quy trình xác thực, điều phối, gia hạn, bảo toàn dữ liệu và kiểm tra tệp tải lên trên `SmartDroneInspection-backend`

---

## 1. Tổng quan công việc đã thực hiện

Sau khi phát hiện lỗi bỏ sót cập nhật số Serial khi Inspector nộp lại hồ sơ đăng ký drone bị từ chối (`resubmit`), toàn bộ các quy trình liên quan từ **FE-01** đến **FE-07** (đăng ký khách hàng, hồ sơ phi công, tài sản công trình, đăng ký/gia hạn drone, báo giá hợp đồng, điều phối ca bay và chốt chặn trước khi cất cánh) đã được rà soát toàn diện.

Qua rà soát và chạy bộ kiểm thử đơn vị, tổng cộng **7 nhóm lỗi / lỗ hổng quy trình** đã được phát hiện, khắc phục triệt để trong mã nguồn Java Backend và bổ sung unit test tự động để bảo vệ lâu dài.

---

## 2. Chi tiết các Lỗi đã Phát hiện & Khắc phục

### 2.1. [FE-02] Bỏ sót cập nhật số Serial và đồng bộ thông số khi nộp lại / gia hạn Drone
- **Vấn đề:**
  1. Khi Inspector bị Manager từ chối hồ sơ đăng ký drone do nhập sai số Serial thân máy (`serialNumber`), việc sửa số Serial ở màn hình *Nộp lại hồ sơ* (`resubmit`) không được lưu vào DB do phương thức `DroneRegistrationApplication.resubmit(...)` và `DroneRegistrationApplicationService.resubmit(...)` không nhận và gán lại `serialNumber`.
  2. Khi gia hạn giấy tờ cho một drone đã duyệt (`droneId != null`), thông tin cập nhật về `model` (chứa thông số MTOW phục vụ phân loại theo NĐ 288/2025/NĐ-CP) và `manufacturer` không được đồng bộ sang bảng `drones`; đồng thời chưa chặn việc gia hạn cho drone đã ở trạng thái `RETIRED`.
- **Khắc phục:**
  - `DroneRegistrationApplication.java`: Bổ sung tham số `serial` vào `resubmit(...)` để cập nhật `serialNumber`.
  - `DroneRegistrationApplicationRepository.java`: Thêm truy vấn `existsBySerialNumberIgnoreCaseAndStatusAndIdNot(...)` để kiểm tra trùng lặp số Serial với các hồ sơ `PENDING` khác khi nộp lại.
  - `DroneRegistrationApplicationService.java`:
    - Cho phép chỉnh sửa `serialNumber` đối với hồ sơ bị từ chối (chưa gắn drone chính thức) và kiểm tra chống trùng lặp với bảng `drones` / hồ sơ `PENDING` khác.
    - Chặn đổi `serialNumber` đối với hồ sơ gia hạn của drone đã được phê duyệt (`CANNOT_CHANGE_APPROVED_DRONE_SERIAL`).
    - Chặn nộp gia hạn hoặc phê duyệt gia hạn đối với drone đã `RETIRED` (`DRONE_RETIRED`).
  - `Drone.java`: Bổ sung `renewRegistration(...)` đồng bộ `model`, `manufacturer`, `registrationNumber`, `registrationFileKey`, `registrationExpiresAt` khi phê duyệt gia hạn.

---

### 2.2. [FE-04 / FE-05] Thiếu chốt chặn hết hạn Bằng lái & Đăng kiểm Drone khi Điều phối & Thực địa
- **Vấn đề:**
  1. `InspectionCreationService.create(...)` chỉ kiểm tra hạng bằng lái (Class A/B), không kiểm tra **ngày hết hạn bằng lái phi công** (`pilotLicenseExpiresAt`) và **ngày hết hạn đăng kiểm drone** (`registrationExpiresAt`) so với ngày bay dự kiến `plannedStartAt`.
  2. `InspectionCreationService.reschedule(...)` khi đổi lịch sang ngày mới không kiểm tra lại hạn bằng lái và hạn đăng kiểm drone theo thời gian bay mới.
  3. `InspectionCreationService.reassign(...)` không kiểm tra phạm vi sở hữu (`organizationId` / `INSPECTOR_PARTNER` & `inspectorOwnerId`) của Inspector/Drone mới, không kiểm tra drone cũ thuộc về đối tác cũ nếu chỉ truyền `newInspectorId`, và không kiểm tra `registrationExpiresAt` của drone.
  4. `InspectionCreationService.uploadFlightPermit(...)` và `InspectionFieldSessionService.start(...)` không kiểm tra xem drone được gán còn ở trạng thái `ACTIVE` hay đã hết hạn đăng kiểm trước khi cho phép gắn phép bay / cất cánh.
- **Khắc phục:**
  - `InspectionCreationService.java`:
    - Bổ sung kiểm tra `PILOT_LICENSE_EXPIRED` và `DRONE_REGISTRATION_EXPIRED` tại `create(...)` và `reschedule(...)` đối chiếu với `plannedStartAt` (và kiểm tra `serviceability == ACTIVE` của drone).
    - Siết chặt phạm vi sở hữu (tổ chức vs đối tác) cho `newInspector` và `drone` tại `reassign(...)`, đồng thời kiểm tra `DRONE_REGISTRATION_EXPIRED` và chặn giữ lại drone của đối tác cũ khi đổi sang đối tác mới.
    - Bổ sung kiểm tra `INVALID_DRONE` và `DRONE_REGISTRATION_EXPIRED` tại `uploadFlightPermit(...)`.
  - `InspectionFieldSessionService.java`:
    - Bổ sung `ObjectProvider<DroneRepository>` để xác minh trước khi `start(...)` ca bay thực địa rằng drone vẫn `ACTIVE` và còn hạn đăng kiểm (`DRONE_REGISTRATION_EXPIRED`).

---

### 2.3. [FE-03 / FE-04] Báo giá & Phân công hợp đồng kiểm tra hạn Drone sai thời điểm
- **Vấn đề:**
  - Trong `ContractWorkflowService.java`, hàm `issueQuote(...)` gọi `partners.isEligibleDrone(input.droneId(), input.inspectorId())` và hàm `assignOccurrence(...)` gọi `partners.lockEligibleDrone(input.droneId(), input.inspectorId())`. Cả hai đều kiểm tra theo `Instant.now()` (thời điểm hiện tại) thay vì thời điểm dự kiến thực hiện ca bay (`firstOccurrenceStartAt` và `plannedStartAt`).
  - Hệ quả: Có thể ký hợp đồng và thanh toán cho một ca bay diễn ra sau vài tháng bằng một chiếc drone sắp hết hạn đăng kiểm sau vài ngày.
- **Khắc phục:**
  - `ContractWorkflowService.java`:
    - Tại `issueQuote(...)`: gọi `partners.isEligibleDrone(input.droneId(), input.inspectorId(), input.firstOccurrenceStartAt())`.
    - Tại `assignOccurrence(...)`: gọi `partners.lockEligibleDrone(input.droneId(), input.inspectorId(), input.plannedStartAt())`.

---

### 2.4. [FE-01] Bế tắc (Deadlock) khi Khách hàng bị Từ chối tọa độ Vùng bay không thể đăng ký lại
- **Vấn đề:**
  - Khách hàng tự đăng ký tài khoản đầu tiên có tọa độ thuộc khu vực cần xét duyệt (`RESTRICTED_ZONE` / `UNLISTED`) được tạo ở trạng thái `DISABLED` trong vùng `PROSPECT_CUSTOMER`.
  - Nếu Admin bấm **Từ chối (Reject)** (do sai tọa độ hoặc thiếu thông tin), email này bị kẹt vĩnh viễn: không thể đăng nhập và khi nộp đơn đăng ký lại thì bị cả `RegistrationOtpService.send(...)` lẫn `OrganizationRegistrationService.register(...)` chặn lỗi `409 EMAIL_ALREADY_EXISTS`.
- **Khắc phục:**
  - `ProspectiveCustomerRegistration.java` & `ProspectiveCustomerRegistrationRepository.java`: Thêm `findByUserId(...)` và phương thức miền `resubmit(...)` (chỉ áp dụng khi trạng thái hiện tại là `REJECTED`).
  - `RegistrationOtpService.java`: Cho phép gửi OTP đăng ký lại nếu tài khoản gắn với email đó là `PROSPECT_CUSTOMER` ở trạng thái `DISABLED` có hồ sơ `REJECTED` (vẫn chặn `409` với hồ sơ `PENDING` hoặc tài khoản đang hoạt động).
  - `OrganizationRegistrationService.java`: Cho phép khách hàng có hồ sơ `REJECTED` đăng ký lại bằng chính email đó:
    - Nếu tọa độ mới vẫn cần xét duyệt: cập nhật thông tin, reset mật khẩu/trạng thái hồ sơ về `PENDING`, ghi log kiểm toán `CUSTOMER_AIRSPACE_REVIEW_RESUBMITTED` và trả về `202 Accepted`.
    - Nếu tọa độ mới đã thuộc `CLEAR_ZONE`: khởi tạo `Organization`, kích hoạt tài khoản (`CUSTOMER_ORGANIZATION`, `ACTIVE`), tạo `Asset` đầu tiên và trả về `201 Created`.

---

### 2.5. [FE-02] Rủi ro mất dữ liệu Bằng lái Phi công khi cập nhật từng phần Hồ sơ Inspector
- **Vấn đề:**
  - Trong `InspectorProfileService.updateProfile(...)`, các trường gửi lên dưới dạng `null` (như thông tin bằng lái, ngày hết hạn bằng, ngày sinh, số CCCD, ghi chú...) bị gán thẳng `null` đè lên giá trị cũ trong DB, dễ làm mất dữ liệu bằng lái nếu gọi API cập nhật từng phần (chỉ sửa số điện thoại/địa chỉ).
- **Khắc phục:**
  - `InspectorProfileService.java`: Bổ sung `resolveOptionalText(...)` và kiểm tra `null` cho các trường ngày (`dateOfBirth`, `pilotLicenseIssuedDate`, `pilotLicenseExpiresAt`):
    - Giá trị `null` (không truyền trong payload) sẽ **giữ nguyên** dữ liệu hiện có trong DB.
    - Chuỗi rỗng `""` truyền chủ động sẽ được chuẩn hóa thành `null` để cho phép xóa trắng trường văn bản từ biểu mẫu đầy đủ trên Web.

---

### 2.6. [FE-02] Lỗ hổng vượt qua kiểm tra Vùng cấm bay (No-Fly Zone) khi sửa từng tọa độ Asset
- **Vấn đề:**
  1. `AssetService.update(...)` chỉ gọi `validateNoFlyZone(...)` khi **cả** `request.latitude()` và `request.longitude()` đều khác `null`. Nếu cập nhật lẻ từng tọa độ (chỉ đổi `latitude` vào vùng cấm bay trong khi giữ nguyên `longitude`), bước kiểm tra vùng cấm bay bị bỏ qua.
  2. `Asset.update(...)` khi cập nhật `locationText` nhưng không gửi kèm `latitude`/`longitude` đã dựng lại JSON vị trí thiếu tọa độ cũ của tài sản.
- **Khắc phục:**
  - `AssetService.java`: Tính tọa độ hiệu lực `(nextLat, nextLon)` kết hợp giữa giá trị mới và giá trị hiện có trên `Asset` để luôn kiểm tra `validateNoFlyZone(nextLat, nextLon)` khi có bất kỳ thay đổi tọa độ nào.
  - `Asset.java`: Dùng `(effectiveLat, effectiveLon)` khi cập nhật chuỗi JSON `locationText`.

---

### 2.7. [Shared / Security] Lỗ hổng bỏ qua kiểm tra Chữ ký Tệp (Magic Bytes) trong `EvidenceUploadValidator`
- **Vấn đề phát hiện khi chạy bộ test:**
  - Bộ test sẵn có `DroneEvidenceUploadServiceTest.rejectsSpoofedContentBeforeStorage` bị **FAILED**.
  - Nguyên nhân: Trong `EvidenceUploadValidator.validate(...)`, các nhánh fallback `else if (declaredType.equals("application/pdf") ...)` cho phép tệp giả mạo chứa byte rác (`{1, 2, 3}`) đi qua miễn là header `Content-Type` khai báo là `application/pdf` hoặc ảnh.
- **Khắc phục:**
  - `EvidenceUploadValidator.java`: Bắt buộc chữ ký nhị phân thực tế (**magic bytes**) phải khớp với PDF (`%PDF-`), PNG (`0x89 PNG`), JPEG (`FF D8 FF`), hoặc WEBP (`RIFF...WEBP`), đồng thời kiểm tra khớp với `Content-Type` khai báo (hoặc `application/octet-stream`/rỗng), loại bỏ hoàn toàn nhánh fallback tin tưởng mù quáng vào `Content-Type`.

---

## 3. Danh sách Tệp đã Sửa đổi & Bổ sung

### Mã nguồn chính (`SmartDroneInspection-backend/src/main/java/...`)
1. `assets/domain/DroneRegistrationApplication.java`
2. `assets/domain/Drone.java`
3. `assets/domain/Asset.java`
4. `assets/repository/DroneRegistrationApplicationRepository.java`
5. `assets/service/DroneRegistrationApplicationService.java`
6. `assets/service/AssetService.java`
7. `contracts/service/ContractWorkflowService.java`
8. `inspections/service/InspectionCreationService.java`
9. `inspections/service/InspectionFieldSessionService.java`
10. `users/domain/ProspectiveCustomerRegistration.java`
11. `users/repository/ProspectiveCustomerRegistrationRepository.java`
12. `users/service/RegistrationOtpService.java`
13. `users/service/OrganizationRegistrationService.java`
14. `users/service/InspectorProfileService.java`
15. `shared/storage/EvidenceUploadValidator.java`

### Kiểm thử tự động (`SmartDroneInspection-backend/src/test/java/...`)
1. `assets/service/DroneRegistrationApplicationServiceTest.java` *(bổ sung 3 test case: sửa serial khi resubmit, chặn trùng serial / đổi serial drone đã duyệt, đồng bộ model khi gia hạn & chặn gia hạn drone `RETIRED`)*
2. `assets/service/AssetServiceTest.java` *(tạo mới: kiểm tra No-Fly Zone khi sửa đơn lẻ 1 tọa độ & bảo toàn tọa độ trong JSON `locationText`)*
3. `contracts/service/ContractWorkflowServiceTest.java` *(cập nhật & bổ sung `issueQuoteChecksDroneEligibilityAtFirstOccurrenceStartAt` + xác minh `lockEligibleDrone(..., assignedStart)`)*
4. `inspections/service/InspectionCreationServiceTest.java` *(tạo mới 4 test case: chặn hết hạn bằng lái/đăng kiểm khi `create`, `reschedule`, `reassign`, `uploadFlightPermit` và kiểm tra sở hữu drone đối tác)*
5. `inspections/service/InspectionFieldSessionDroneGuardTest.java` *(tạo mới: chặn `start` ca bay khi drone hết hạn đăng kiểm hoặc không `ACTIVE`)*
6. `users/InspectorProfileServiceTest.java` *(bổ sung `updateProfile_preservesExistingLicenseFieldsWhenOmitted`)*
7. `users/OrganizationRegistrationServiceTest.java` *(tạo mới 4 test case: đăng ký lại khi bị từ chối vùng bay sang `PENDING_AIRSPACE_REVIEW` và `CLEAR_ZONE`, chặn ghi đè hồ sơ `PENDING`/`ACTIVE`, và kiểm tra gửi OTP cho hồ sơ bị từ chối)*

---

## 4. Kết quả Kiểm chứng Thực tế (Verification)

### Lệnh đã thực thi tại `SmartDroneInspection-backend`
1. Định dạng mã nguồn (Google Java Format):
   ```powershell
   ./mvnw spotless:apply
   ```
   -> **BUILD SUCCESS** (`spotless:check` đạt 607/607 files).

2. Chạy toàn bộ Unit Tests liên quan & Spring Modulith Boundary Test:
   ```powershell
   ./mvnw test -Dtest="DroneRegistrationApplicationServiceTest,DroneServiceTest,AssetServiceTest,AirspaceAdvisoryServiceTest,DroneEvidenceUploadServiceTest,ContractWorkflowServiceTest,PartnerRegistryServiceTest,Mf2InspectionAssignmentAdapterTest,InspectorProfileServiceTest,OrganizationRegistrationServiceTest,AdminUserServiceTest,InspectorPartnerLicenseDocumentServiceTest,InspectionCreationServiceTest,InspectionFieldSessionDroneGuardTest,ModulithArchitectureTest,WorkOrderServiceTest,MaintenanceExecutionServiceTest"
   ```
   -> **BUILD SUCCESS — 93/93 tests PASSED** (`Failures: 0, Errors: 0, Skipped: 0`), cụ thể:
   - `AirspaceAdvisoryServiceTest`: 5/5 PASSED
   - `DroneEvidenceUploadServiceTest`: 5/5 PASSED *(đã phục hồi `rejectsSpoofedContentBeforeStorage`)*
   - `AssetServiceTest`: 1/1 PASSED
   - `DroneRegistrationApplicationServiceTest`: 11/11 PASSED
   - `ContractWorkflowServiceTest`: 33/33 PASSED
   - `Mf2InspectionAssignmentAdapterTest`: 4/4 PASSED
   - `PartnerRegistryServiceTest`: 6/6 PASSED
   - `InspectionCreationServiceTest`: 4/4 PASSED
   - `InspectionFieldSessionDroneGuardTest`: 1/1 PASSED
   - `MaintenanceExecutionServiceTest`: 6/6 PASSED
   - `WorkOrderServiceTest`: 1/1 PASSED
   - `ModulithArchitectureTest`: 3/3 PASSED *(không vi phạm ranh giới Spring Modulith)*
   - `AdminUserServiceTest`: 1/1 PASSED
   - `InspectorPartnerLicenseDocumentServiceTest`: 2/2 PASSED
   - `InspectorProfileServiceTest`: 6/6 PASSED
   - `OrganizationRegistrationServiceTest`: 4/4 PASSED

### Giới hạn môi trường & Lưu ý kiểm thử tiếp theo
- Trên máy hiện tại, **Docker Desktop daemon không chạy** (`failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine`), nên các bài test tích hợp dùng Testcontainers PostgreSQL/MinIO (`*ApiIntegrationTest`) và lệnh `./mvnw verify` đầy đủ (kèm cổng JaCoCo 80%) **chưa được thực thi** trong phiên này.
- Khi có Docker chạy, cần thực thi lại lệnh chuẩn sau để xác nhận toàn bộ tầng tích hợp và cập nhật trạng thái Round 3 trong Report 5:
  ```powershell
  cd SmartDroneInspection-backend
  docker compose up -d
  ./mvnw verify
  ```
