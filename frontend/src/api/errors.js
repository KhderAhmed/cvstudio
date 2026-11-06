/**
 * يحوّل خطأ axios/DRF إلى رسالة قابلة للقراءة بدل JSON خام.
 * أمثلة على ما يرجعه DRF:
 *   {"detail": "..."}                      → "..."
 *   {"full_name": ["هذا الحقل مطلوب."]}    → "full_name: هذا الحقل مطلوب."
 */
export function apiError(err, fallback = 'حدث خطأ غير متوقع') {
  if (!err?.response) return 'تعذّر الاتصال بالخادم'

  const data = err.response.data
  if (!data) return fallback
  if (typeof data === 'string') return data.length < 200 ? data : fallback
  if (data.detail) return String(data.detail)

  const parts = []
  for (const [field, value] of Object.entries(data)) {
    const msg = Array.isArray(value) ? value[0] : value
    if (typeof msg === 'string') {
      parts.push(field === 'non_field_errors' ? msg : `${field}: ${msg}`)
    }
  }
  return parts.length ? parts.slice(0, 3).join(' | ') : fallback
}
