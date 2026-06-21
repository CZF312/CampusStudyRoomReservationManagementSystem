/**
 * 【F4-1·步骤2】实例：内容为小明学号纯文本，供 admin 拍照 jsQR 识别
 */
import QRCode from 'qrcode'

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
