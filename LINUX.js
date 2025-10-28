const axios = require('axios');
const fs = require('fs');
const readline = require('readline-sync');

// Konfigurasi - menggunakan endpoint yang sama dengan website
const REPORT_API_URL = 'https://www.tiktok.com/api/report/feedback/';
const EMAIL = 'hozoonetwork@gmail.com';
const REPORTER_NAME = 'LORDHOZOO';

class TikTokAutoReporter {
    constructor() {
        this.reportCount = 0;
        this.successCount = 0;
        this.failedCount = 0;
        this.isRunning = false;
        
        // Headers yang sama persis dengan browser
        this.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://www.tiktok.com',
            'Referer': 'https://www.tiktok.com/legal/report/feedback?lang=id-ID',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Priority': 'u=1, i',
            'Connection': 'keep-alive'
        };
    }

    // Generate CSRF token (simulasi)
    generateCSRFToken() {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        let token = '';
        for (let i = 0; i < 32; i++) {
            token += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return token;
    }

    // Generate random delay
    randomDelay(min = 50, max = 200) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    // Generate session ID
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    // Generate report payload sesuai format TikTok
    generateReportPayload(username, reportType = 1004) {
        // Format payload sesuai dengan yang dikirim website TikTok
        const payload = {
            'object_id': username,
            'owner_id': '', // Biasanya kosong untuk user report
            'object_type': '1', // 1 = User, 2 = Video, 3 = Comment, 4 = Live
            'report_type': reportType.toString(),
            'report_desc': this.generateReportDescription(username, reportType),
            'report_scene': '1000', // Scene report
            'feedback_type': '100001', // Type feedback
            'contact': EMAIL,
            'reporter_username': REPORTER_NAME,
            'reporter_id': '', // Kosong untuk anonymous
            'lang': 'id_ID',
            'app_language': 'id_ID',
            'priority_region': '',
            'region': 'ID',
            'timezone_name': 'Asia/Jakarta'
        };

        return this.serializeFormData(payload);
    }

    // Serialize data ke format x-www-form-urlencoded
    serializeFormData(data) {
        return Object.keys(data)
            .map(key => encodeURIComponent(key) + '=' + encodeURIComponent(data[key]))
            .join('&');
    }

    // Generate report description berdasarkan type
    generateReportDescription(username, reportType) {
        const descriptions = {
            1001: `Akun @${username} terlibat dalam aktivitas ilegal dan melanggar hukum yang berlaku. Konten yang dibagikan mengandung unsur kriminal dan dapat membahayakan masyarakat.`,
            1002: `User @${username} diduga kuat terlibat dalam eksploitasi anak di bawah umur dan penyebaran konten kekerasan terhadap anak. Sangat berbahaya dan melanggar UU Perlindungan Anak.`,
            1003: `Akun @${username} menyebarkan ujaran kebencian, diskriminasi, dan konten rasis yang dapat memecah belah persatuan bangsa.`,
            1004: `@${username} secara terang-terangan mengunggah konten pornografi eksplisit, video seksual, dan materi dewasa yang tidak pantas untuk platform TikTok.`,
            1005: `User @${username} terindikasi sebagai bagian dari kelompok ekstremis yang menyebarkan paham radikal dan konten kekerasan.`,
            1006: `Akun @${username} melakukan pelecehan, perundungan, dan intimidasi terhadap pengguna lain secara sistematis.`,
            1007: `@${username} membagikan konten yang mendorong perilaku bunuh diri dan melukai diri sendiri yang sangat berbahaya bagi mental health pengguna.`,
            1008: `User @${username} melakukan challenge dan aksi berbahaya yang dapat mengancam keselamatan jiwa pengikutnya.`,
            1010: `Akun @${username} adalah penipu yang melakukan scam, phishing, dan pencurian data pengguna.`,
            1011: `@${username} melakukan spam massal, botting, dan penyalahgunaan platform untuk keuntungan tidak sah.`
        };

        return descriptions[reportType] || `Akun @${username} melanggar kebijakan komunitas TikTok dengan konten yang tidak pantas dan berbahaya bagi pengguna.`;
    }

    // Get report types sesuai TikTok
    getReportTypes() {
        return {
            1001: "Aktivitas Ilegal",
            1002: "Eksploitasi Anak", 
            1003: "Ujaran Kebencian",
            1004: "Konten Tidak Pantas",
            1005: "Ekstremisme Kekerasan",
            1006: "Pelecehan & Perundungan",
            1007: "Bunuh Diri & Melukai Diri",
            1008: "Aksi Berbahaya",
            1010: "Penipuan",
            1011: "Spam"
        };
    }

    // Get random report type
    getRandomReportType() {
        const types = Object.keys(this.getReportTypes());
        return parseInt(types[Math.floor(Math.random() * types.length)]);
    }

    // Send report via TikTok API
    async sendReport(username) {
        try {
            const reportType = this.getRandomReportType();
            const payload = this.generateReportPayload(username, reportType);
            
            // Dynamic headers dengan session fresh setiap request
            const dynamicHeaders = {
                ...this.headers,
                'X-Secsdk-Csrf-Token': this.generateCSRFToken(),
                'X-Requested-With': 'XMLHttpRequest',
                'Cookie': `sessionid=${this.generateSessionId()}; lang=en;`,
                'Tt-Webid': Math.random().toString(36).substr(2, 19),
                'Tt-Csrf-Token': this.generateCSRFToken()
            };

            console.log(`📤 Mengirim report untuk @${username} (Type: ${reportType})...`);

            const response = await axios.post(REPORT_API_URL, payload, {
                headers: dynamicHeaders,
                timeout: 15000,
                maxRedirects: 0,
                validateStatus: function (status) {
                    return status >= 200 && status < 500;
                }
            });

            this.reportCount++;

            // Handle response sesuai format TikTok
            if (response.status === 200) {
                const responseData = response.data;
                
                if (responseData && responseData.success) {
                    this.successCount++;
                    console.log(`✅ [${this.reportCount}] SUCCESS: Report @${username} diterima!`);
                    return true;
                } else if (responseData && responseData.msg) {
                    console.log(`⚠️ [${this.reportCount}] WARNING: ${responseData.msg}`);
                    return false;
                } else {
                    // Jika tidak ada response data tapi status 200, anggap success
                    this.successCount++;
                    console.log(`✅ [${this.reportCount}] SUCCESS: Report @${username} (Status: ${response.status})`);
                    return true;
                }
            } else if (response.status === 429) {
                console.log(`🚫 [${this.reportCount}] RATE LIMITED: Terlalu banyak request, tunggu sebentar...`);
                await new Promise(resolve => setTimeout(resolve, 5000));
                return false;
            } else {
                this.failedCount++;
                console.log(`❌ [${this.reportCount}] FAILED: Status ${response.status} | ${response.statusText}`);
                return false;
            }

        } catch (error) {
            this.reportCount++;
            this.failedCount++;
            
            if (error.response) {
                // Error dengan response dari server
                console.log(`💀 [${this.reportCount}] SERVER ERROR: ${error.response.status} - ${error.response.statusText}`);
            } else if (error.request) {
                // Error tanpa response
                console.log(`🌐 [${this.reportCount}] NETWORK ERROR: Tidak ada response dari server`);
            } else {
                // Error lainnya
                console.log(`🐛 [${this.reportCount}] UNKNOWN ERROR: ${error.message}`);
            }
            
            return false;
        }
    }

    // Unlimited report dengan optimasi
    async startUnlimitedReport(username) {
        this.isRunning = true;
        console.log(`\n🚀 MEMULAI UNLIMITED REPORT UNTUK: @${username}`);
        console.log('📍 Using Official TikTok API Endpoint');
        console.log('⏹️  Tekan Ctrl+C untuk berhenti\n');

        let consecutiveErrors = 0;
        const maxConsecutiveErrors = 5;

        while (this.isRunning) {
            try {
                const success = await this.sendReport(username);
                
                if (success) {
                    consecutiveErrors = 0;
                } else {
                    consecutiveErrors++;
                    if (consecutiveErrors >= maxConsecutiveErrors) {
                        console.log('🔄 Too many errors, taking a longer break...');
                        await new Promise(resolve => setTimeout(resolve, 10000));
                        consecutiveErrors = 0;
                    }
                }

                // Dynamic delay based on performance
                const delay = this.randomDelay(30, 150);
                await new Promise(resolve => setTimeout(resolve, delay));
                
                // Status update
                if (this.reportCount % 10 === 0) {
                    const successRate = ((this.successCount / this.reportCount) * 100).toFixed(1);
                    console.log(`\n📊 [LIVE STATS] Total: ${this.reportCount} | Success: ${this.successCount} | Failed: ${this.failedCount} | Rate: ${successRate}%\n`);
                }
                
            } catch (error) {
                console.log(`🌀 Loop Error: ${error.message}`);
                consecutiveErrors++;
                await new Promise(resolve => setTimeout(resolve, 2000));
            }
        }
    }

    // Multiple accounts report
    async startMultipleReports(usernames) {
        this.isRunning = true;
        console.log(`\n🚀 MEMULAI MASS REPORT UNTUK ${usernames.length} AKUN`);
        
        let accountIndex = 0;
        let consecutiveErrors = 0;

        while (this.isRunning) {
            const username = usernames[accountIndex];
            
            try {
                const success = await this.sendReport(username);
                
                if (success) {
                    consecutiveErrors = 0;
                } else {
                    consecutiveErrors++;
                }

                // Rotate to next account
                accountIndex = (accountIndex + 1) % usernames.length;
                
                // Dynamic delay
                await new Promise(resolve => setTimeout(resolve, this.randomDelay(25, 100)));
                
                // Status update
                if (this.reportCount % 15 === 0) {
                    const successRate = ((this.successCount / this.reportCount) * 100).toFixed(1);
                    console.log(`\n📊 [ROTATION STATS] Total: ${this.reportCount} | Success: ${successRate}% | Current: @${username}\n`);
                }
                
            } catch (error) {
                console.log(`🌀 Rotation Error: ${error.message}`);
                consecutiveErrors++;
                await new Promise(resolve => setTimeout(resolve, 3000));
            }
        }
    }

    // Show detailed banner
    showBanner() {
        console.log(`
╔══════════════════════════════════════════════════════════════╗
║ 🚀 TIKTOK UNLIMITED AUTO-REPORT TOOL                        ║
║ 📍 Using Official API: ${REPORT_API_URL} ║
║ 👤 Reporter: ${REPORTER_NAME}                              ║
║ 📧 Email: ${EMAIL}                          ║
║ 🕒 Started: ${new Date().toLocaleString('id-ID')}              ║
╚══════════════════════════════════════════════════════════════╝
        `);
    }

    // Show report types
    showReportTypes() {
        console.log('\n📋 JENIS PELAPORAN YANG TERSEDIA:');
        const types = this.getReportTypes();
        Object.keys(types).forEach(key => {
            console.log(`   ${key}: ${types[key]}`);
        });
        console.log('');
    }

    // Main menu
    async showMenu() {
        this.showBanner();
        this.showReportTypes();
        
        console.log('=== 🎯 MODE OPERASI ===');
        console.log('1. 🚀 UNLIMITED MODE - Satu target, report unlimited');
        console.log('2. 🔄 MASS ROTATION - Multiple targets, rotating report'); 
        console.log('3. 📊 SHOW STATISTICS');
        console.log('4. ❌ EXIT');
        
        const choice = readline.question('Pilih mode (1-4): ');
        
        switch (choice) {
            case '1':
                const singleUsername = readline.question('Masukkan username target (tanpa @): ').trim();
                if (singleUsername) {
                    await this.startUnlimitedReport(singleUsername);
                } else {
                    console.log('❌ Username tidak boleh kosong!');
                    await this.showMenu();
                }
                break;
                
            case '2':
                const usernamesInput = readline.question('Masukkan usernames (pisahkan dengan koma): ');
                const usernames = usernamesInput.split(',')
                    .map(u => u.trim().replace('@', ''))
                    .filter(u => u.length > 0);
                
                if (usernames.length > 0) {
                    await this.startMultipleReports(usernames);
                } else {
                    console.log('❌ Tidak ada username yang valid!');
                    await this.showMenu();
                }
                break;
                
            case '3':
                this.showStatistics();
                await this.showMenu();
                break;
                
            case '4':
                console.log('👋 Keluar dari program...');
                process.exit(0);
                break;
                
            default:
                console.log('❌ Pilihan tidak valid!');
                await this.showMenu();
        }
    }

    // Show statistics
    showStatistics() {
        console.log('\n📈 CURRENT STATISTICS:');
        console.log(`   Total Reports Sent: ${this.reportCount}`);
        console.log(`   Successful: ${this.successCount}`);
        console.log(`   Failed: ${this.failedCount}`);
        if (this.reportCount > 0) {
            const successRate = ((this.successCount / this.reportCount) * 100).toFixed(2);
            console.log(`   Success Rate: ${successRate}%`);
        }
        console.log(`   Running: ${this.isRunning ? 'YES' : 'NO'}`);
    }

    // Handle shutdown gracefully
    setupShutdownHandler() {
        process.on('SIGINT', () => {
            console.log('\n\n🛑 PROGRAM DIHENTIKAN OLEH USER');
            console.log('📊 FINAL REPORT STATISTICS:');
            this.showStatistics();
            console.log('\n⚠️  Catatan: Report mungkin masih diproses oleh sistem TikTok');
            console.log('📧 Email followup: ' + EMAIL);
            this.isRunning = false;
            setTimeout(() => process.exit(0), 1000);
        });
    }

    // Run application
    async run() {
        this.setupShutdownHandler();
        await this.showMenu();
    }
}

// Run the auto-reporter
console.log('🔧 Initializing TikTok Auto-Reporter...');
const autoReporter = new TikTokAutoReporter();
autoReporter.run().catch(console.error);
