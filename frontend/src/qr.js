/**
 * 【F4-1·签到】功能链实例：小明签到 Tab 显示学号 **202225220101** 与 QR → 管理员输入学号（或拍照 jsQR 识别）→ 预约变「使用中」→ 信用 **+5**。 本处职责：内容为小明学号纯文本，供 admin 拍照 jsQR 识别
 */
import QRCode from 'qrcode' // 【行】执行本行语句，推进功能链中的当前步骤

/**
 * @param {string} text 学号等纯文本（实例：202225220101）
 * @returns {Promise<string>} SVG 字符串，嵌入学生签到页
 */
export async function createQrSvg(text) {
  return QRCode.toString(String(text), {
    type: 'svg',
    margin: 2,
    width: 240,
    errorCorrectionLevel: 'M',
    color: { dark: '#000000', light: '#ffffff' }
  })
}
