/**
 * 【F4-1·签到】功能链实例：小明签到 Tab 显示学号 **202225220101** 与 QR → 管理员输入学号（或拍照 jsQR 识别）→ 预约变「使用中」→ 信用 **+5**。 本处职责：内容为小明学号纯文本，供 admin 拍照 jsQR 识别
 */
import QRCode from 'qrcode' // 【行】执行本行语句，推进功能链中的当前步骤

/**
 * @param {string} text 学号等纯文本（实例：202225220101）
 * @returns {Promise<string>} SVG 字符串，嵌入学生签到页
 */
export async function createQrSvg(text) { // 【行】进入代码块
  return QRCode.toString(String(text), { // 【行】返回本函数计算结果给调用方
    type: 'svg', // 【行】执行本行语句，推进功能链中的当前步骤
    margin: 2, // 【行】执行本行语句，推进功能链中的当前步骤
    width: 240, // 【行】执行本行语句，推进功能链中的当前步骤
    errorCorrectionLevel: 'M', // 【行】执行本行语句，推进功能链中的当前步骤
    color: { dark: '#000000', light: '#ffffff' }
  }) // 【行】执行本行语句，推进功能链中的当前步骤
}
