/**
 * ينسخ نصاً للحافظة. navigator.clipboard يعمل فقط على HTTPS أو localhost،
 * لذلك نستخدم بديلاً (execCommand) عند فتح الموقع عبر HTTP.
 * يرجع true عند النجاح.
 */
export async function copyText(text) {
  try {
    if (navigator.clipboard?.writeText && window.isSecureContext) {
      await navigator.clipboard.writeText(text)
      return true
    }
  } catch {
    /* ننتقل للبديل */
  }

  try {
    const el = document.createElement('textarea')
    el.value = text
    el.setAttribute('readonly', '')
    el.style.position = 'fixed'
    el.style.opacity = '0'
    document.body.appendChild(el)
    el.select()
    const ok = document.execCommand('copy')
    document.body.removeChild(el)
    return ok
  } catch {
    return false
  }
}
