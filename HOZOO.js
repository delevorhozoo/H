const axios = require('axios');
const readline = require('readline-sync');
const fs = require('fs');

// Konfigurasi
const REPORT_URL = 'https://www.tiktok.com/legal/report/feedback?lang=id-ID&enter_method=bottom_navigation';
const EMAIL = 'hozoonetwork@gmail.com';
const REPORTER_NAME = 'LORDHOZOO';

class TikTokReporter {
    constructor() {
        this.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'id-ID,id;q=0.9,en;q=0.8',
            'Origin': 'https://www.tiktok.com',
            'Referer': 'https://www.tiktok.com/legal/report/feedback'
        };
    }

    // Input data dari user
    getReportData() {
        console.log('=== TIKTOK REPORT TOOL ===\n');
        
        const username = readline.question('Masukkan username TikTok (contoh: @username): ');
        const displayName = readline.question('Masukkan display name: ');
        
        console.log('\nJenis Pelanggaran:');
        console.log('1. Konten Pornografi/Eksplisit');
        console.log('2. Penipuan/Scam');
        console.log('3. Pelecehan/Bullying');
        console.log('4. Spam');
        console.log('5. Lainnya');
        
        const violationType = readline.question('Pilih jenis pelanggaran (1-5): ');
        
        const additionalInfo = readline.question('Info tambahan (opsional): ');
        
        return {
            username,
            displayName,
            violationType,
            additionalInfo
        };
    }

    // Generate report message
    generateReportMessage(data) {
        const violationTypes = {
            '1': 'Konten Pornografi/Eksplisit',
            '2': 'Penipuan/Scam', 
            '3': 'Pelecehan/Bullying',
            '4': 'Spam',
            '5': 'Pelanggaran Lainnya'
        };

        const violationDesc = violationTypes[data.violationType] || 'Pelanggaran Kebijakan TikTok';

        return `
Kepada Tim Trust & Safety TikTok,

Saya ingin melaporkan akun dengan detail berikut:

Nama Pengguna (Username): ${data.username}
Nama Akun (Display Name): ${data.displayName}

Akun tersebut secara terang-terangan dan berulang kali melakukan pelanggaran ${violationDesc} yang melanggar pedoman komunitas TikTok.

${this.getViolationDetails(data.violationType)}

${data.additionalInfo ? `Info tambahan: ${data.additionalInfo}` : ''}

Dengan ini, saya mendesak TikTok untuk segera mengambil tindakan tegas dengan:
1. MENGHAPUS semua konten pelanggaran dari akun tersebut
2. MEMBLOKIR PERMANEN akun tersebut dari platform

Konten semacam ini sangat berbahaya, terutama bagi pengguna di bawah umur, dan merusak lingkungan yang aman di TikTok. Tindakan yang cepat dan tegas sangat diharapkan.

Terima kasih atas perhatiannya.

Salam,
${REPORTER_NAME}
Email: ${EMAIL}
        `.trim();
    }

    getViolationDetails(type) {
        const details = {
            '1': `Konten-konten yang diunggah oleh akun ini termasuk:
- Video dan gambar yang menampilkan aktivitas seksual eksplisit
- Tautan yang mengarah ke situs dewasa  
- Komentar atau caption yang bersifat porno dan melecehkan`,

            '2': `Akun ini terlibat dalam aktivitas penipuan termasuk:
- Menipu pengguna dengan janji palsu
- Mengirim link phishing atau scam
- Memanipulasi data pengguna`,

            '3': `Akun ini melakukan pelecehan termasuk:
- Komentar hate speech dan bullying
- Intimidasi terhadap pengguna lain
- Konten yang mendorong kekerasan`,

            '4': `Akun ini melakukan spam termasuk:
- Mengirim komentar spam berulang
- Mengikuti/meng-unfollow massal
- Posting konten duplikat berlebihan`,

            '5': `Akun ini melanggar kebijakan komunitas TikTok dengan:
- Perilaku tidak pantas dan mengganggu
- Konten yang tidak sesuai untuk semua umur
- Aktivitas mencurigakan lainnya`
        };

        return details[type] || 'Akun ini melakukan pelanggaran serius terhadap kebijakan komunitas TikTok.';
    }

    // Simpan report ke file
    saveReportToFile(reportData, message) {
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const filename = `tiktok_report_${timestamp}.txt`;
        
        const fileContent = `
TIKTOK REPORT - ${timestamp}
==============================

DATA PELAPOR:
- Nama: ${REPORTER_NAME}
- Email: ${EMAIL}
- Waktu: ${new Date().toLocaleString('id-ID')}

DATA AKUN YANG DILAPORKAN:
- Username: ${reportData.username}
- Display Name: ${reportData.displayName}
- Jenis Pelanggaran: ${reportData.violationType}

ISI LAPORAN:
${message}

STATUS: TERSIMPAN OFFLINE
        `.trim();

        fs.writeFileSync(filename, fileContent);
        console.log(`\n✅ Report disimpan sebagai: ${filename}`);
        return filename;
    }

    // Tampilkan preview
    showPreview(reportData, message) {
        console.log('\n' + '='.repeat(50));
        console.log('PREVIEW LAPORAN:');
        console.log('='.repeat(50));
        console.log(message);
        console.log('='.repeat(50));
        
        const confirm = readline.question('\nKirim laporan? (y/n): ');
        return confirm.toLowerCase() === 'y';
    }

    // Main function
    async run() {
        try {
            // Get report data
            const reportData = this.getReportData();
            
            // Generate message
            const reportMessage = this.generateReportMessage(reportData);
            
            // Show preview
            const confirmed = this.showPreview(reportData, reportMessage);
            
            if (confirmed) {
                console.log('\n🔄 Mengirim laporan...');
                
                // Save to file first
                const filename = this.saveReportToFile(reportData, reportMessage);
                
                console.log('\n✅ Laporan berhasil dibuat dan disimpan!');
                console.log(`📁 File: ${filename}`);
                console.log('\n📧 Untuk mengirim, silakan:');
                console.log('1. Buka: https://www.tiktok.com/legal/report/feedback');
                console.log('2. Copy-paste laporan dari file di atas');
                console.log('3. Isi form dengan data yang sesuai');
                
            } else {
                console.log('\n❌ Laporan dibatalkan.');
            }
            
        } catch (error) {
            console.error('\n❌ Error:', error.message);
        }
    }
}

// Run the tool
const reporter = new TikTokReporter();
reporter.run();
