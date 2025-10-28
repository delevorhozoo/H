const axios = require('axios');
const fs = require('fs');
const readline = require('readline-sync');

// Konfigurasi
const REPORT_API_URL = 'https://www.tiktok.com/api/report/feedback/';
const TIKTOK_REPORT_URL = 'https://www.tiktok.com/legal/report/feedback?lang=id-ID';
const EMAIL = 'hozoonetwork@gmail.com';
const REPORTER_NAME = 'LORDHOZOO';

class TikTokAutoReporter {
    constructor() {
        this.reportCount = 0;
        this.successCount = 0;
        this.failedCount = 0;
        this.isRunning = false;
        this.csrfToken = '';
        this.sessionId = '';
        this.ttWebId = '';
        
        this.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://www.tiktok.com',
            'Referer': TIKTOK_REPORT_URL,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Priority': 'u=1, i',
            'Connection': 'keep-alive'
        };
    }

    // Ambil token dan session asli dari TikTok
    async fetchRealTokens() {
        try {
            console.log('🔑 Mengambil token asli dari TikTok...');
            
            const response = await axios.get(TIKTOK_REPORT_URL, {
                headers: {
                    'User-Agent': this.headers['User-Agent'],
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
                },
                timeout: 10000,
                maxRedirects: 5
            });

            // Extract cookies dari response headers
            const setCookieHeaders = response.headers['set-cookie'];
            if (setCookieHeaders) {
                for (const cookieHeader of setCookieHeaders) {
                    if (cookieHeader.includes('csrf_token')) {
                        this.csrfToken = cookieHeader.match(/csrf_token=([^;]+)/)?.[1] || '';
                    }
                    if (cookieHeader.includes('sessionid')) {
                        this.sessionId = cookieHeader.match(/sessionid=([^;]+)/)?.[1] || '';
                    }
                    if (cookieHeader.includes('tt_webid')) {
                        this.ttWebId = cookieHeader.match(/tt_webid=([^;]+)/)?.[1] || '';
                    }
                    if (cookieHeader.includes('tt_csrf_token')) {
                        this.csrfToken = cookieHeader.match(/tt_csrf_token=([^;]+)/)?.[1] || this.csrfToken;
                    }
                }
            }

            // Juga cari token di HTML body
            const html = response.data;
            const csrfMatch = html.match(/<meta[^>]*csrf-token[^>]*content="([^"]*)"/i) || 
                            html.match(/window\.csrfToken\s*=\s*['"]([^'"]+)['"]/i) ||
                            html.match(/["']csrf_token["']\s*:\s*["']([^"']+)["']/i);
            
            if (csrfMatch && csrfMatch[1]) {
                this.csrfToken = csrfMatch[1];
            }

            // Generate tt_webid jika tidak ditemukan
            if (!this.ttWebId) {
                this.ttWebId = this.generateTTWebId();
            }

            // Generate session ID jika tidak ditemukan
            if (!this.sessionId) {
                this.sessionId = this.generateSessionId();
            }

            console.log('✅ Token berhasil diambil:');
            console.log(`   CSRF Token: ${this.csrfToken ? '✓' : '✗'}`);
            console.log(`   Session ID: ${this.sessionId ? '✓' : '✗'}`);
            console.log(`   TT Web ID: ${this.ttWebId ? '✓' : '✗'}`);

            return true;

        } catch (error) {
            console.log('❌ Gagal mengambil token asli, menggunakan fallback...');
            this.useFallbackTokens();
            return false;
        }
    }

    // Fallback tokens jika gagal ambil yang asli
    useFallbackTokens() {
        this.csrfToken = this.generateRealCSRFToken();
        this.sessionId = this.generateSessionId();
        this.ttWebId = this.generateTTWebId();
        console.log('🔄 Menggunakan fallback tokens');
    }

    // Generate CSRF token yang lebih realistik
    generateRealCSRFToken() {
        const crypto = require('crypto');
        return crypto.randomBytes(32).toString('hex');
    }

    // Generate TT Web ID sesuai format TikTok
    generateTTWebId() {
        const crypto = require('crypto');
        const timestamp = Date.now();
        const random = crypto.randomBytes(8).toString('hex');
        return `7${timestamp.toString().substr(0, 12)}${random.substr(0, 16)}`;
    }

    // Generate session ID
    generateSessionId() {
        const crypto = require('crypto');
        return 'sid_' + crypto.randomBytes(16).toString('hex');
    }

    // Generate random delay
    randomDelay(min = 100, max = 300) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    // Generate report payload sesuai format TikTok asli
    generateReportPayload(username, reportType = 1004) {
        const payload = {
            'object_id': username,
            'owner_id': '',
            'object_type': '1',
            'report_type': reportType.toString(),
            'report_desc': this.generateReportDescription(username, reportType),
            'report_scene': '1000',
            'feedback_type': '100001',
            'contact': EMAIL,
            'reporter_username': REPORTER_NAME,
            'reporter_id': '',
            'lang': 'id_ID',
            'app_language': 'id_ID',
            'priority_region': '',
            'region': 'ID',
            'timezone_name': 'Asia/Jakarta',
            'timestamp': Date.now().toString()
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

    // Build cookies string
    buildCookies() {
        const cookies = [];
        if (this.sessionId) cookies.push(`sessionid=${this.sessionId}`);
        if (this.ttWebId) cookies.push(`tt_webid=${this.ttWebId}`);
        if (this.csrfToken) cookies.push(`csrf_token=${this.csrfToken}`);
        if (this.csrfToken) cookies.push(`tt_csrf_token=${this.csrfToken}`);
        cookies.push('lang=en');
        return cookies.join('; ');
    }

    // Send report via TikTok API dengan token asli
    async sendReport(username) {
        try {
            // Refresh tokens setiap 50 reports
            if (this.reportCount % 50 === 0) {
                await this.fetchRealTokens();
            }

            const reportType = this.getRandomReportType();
            const payload = this.generateReportPayload(username, reportType);
            
            // Build headers dengan token asli
            const dynamicHeaders = {
                ...this.headers,
                'X-CSRFToken': this.csrfToken,
                'X-Tt-Token': this.csrfToken,
                'X-Secsdk-Csrf-Token': this.csrfToken,
                'X-Requested-With': 'XMLHttpRequest',
                'Cookie': this.buildCookies(),
                'Tt-Webid': this.ttWebId,
                'Tt-Csrf-Token': this.csrfToken
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

            // Handle response
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
                    this.successCount++;
                    console.log(`✅ [${this.reportCount}] SUCCESS: Report @${username} (Status: ${response.status})`);
                    return true;
                }
            } else if (response.status === 429) {
                console.log(`🚫 [${this.reportCount}] RATE LIMITED: Tunggu 10 detik...`);
                await new Promise(resolve => setTimeout(resolve, 10000));
                return false;
            } else if (response.status === 403) {
                console.log(`🔑 [${this.reportCount}] TOKEN EXPIRED: Refresh tokens...`);
                await this.fetchRealTokens();
                return false;
            } else {
                this.failedCount++;
                console.log(`❌ [${this.reportCount}] FAILED: Status ${response.status}`);
                return false;
            }

        } catch (error) {
            this.reportCount++;
            this.failedCount++;
            
            if (error.code === 'ECONNRESET') {
                console.log(`🔌 [${this.reportCount}] CONNECTION RESET`);
            } else if (error.code === 'ETIMEDOUT') {
                console.log(`⏰ [${this.reportCount}] TIMEOUT`);
            } else if (error.response) {
                console.log(`💀 [${this.reportCount}] SERVER ERROR: ${error.response.status}`);
            } else if (error.request) {
                console.log(`🌐 [${this.reportCount}] NETWORK ERROR`);
            } else {
                console.log(`🐛 [${this.reportCount}] ERROR: ${error.message}`);
            }
            
            return false;
        }
    }

    // Unlimited report dengan token management
    async startUnlimitedReport(username) {
        // Ambil token asli pertama kali
        await this.fetchRealTokens();
        
        this.isRunning = true;
        console.log(`\n🚀 MEMULAI UNLIMITED REPORT UNTUK: @${username}`);
        console.log('📍 Menggunakan Token Asli dari TikTok');
        console.log('⏹️  Tekan Ctrl+C untuk berhenti\n');

        let consecutiveErrors = 0;
        const maxConsecutiveErrors = 3;

        while (this.isRunning) {
            try {
                const success = await this.sendReport(username);
                
                if (success) {
                    consecutiveErrors = 0;
                } else {
                    consecutiveErrors++;
                    if (consecutiveErrors >= maxConsecutiveErrors) {
                        console.log('🔄 Refresh tokens karena banyak error...');
                        await this.fetchRealTokens();
                        consecutiveErrors = 0;
                        await new Promise(resolve => setTimeout(resolve, 5000));
                    }
                }

                const delay = this.randomDelay(80, 200);
                await new Promise(resolve => setTimeout(resolve, delay));
                
                if (this.reportCount % 10 === 0) {
                    const successRate = ((this.successCount / this.reportCount) * 100).toFixed(1);
                    console.log(`\n📊 [LIVE] Total: ${this.reportCount} | Success: ${this.successCount} | Failed: ${this.failedCount} | Rate: ${successRate}%\n`);
                }
                
            } catch (error) {
                console.log(`🌀 Loop Error: ${error.message}`);
                consecutiveErrors++;
                await new Promise(resolve => setTimeout(resolve, 3000));
            }
        }
    }

    // Multiple accounts report
    async startMultipleReports(usernames) {
        await this.fetchRealTokens();
        
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

                accountIndex = (accountIndex + 1) % usernames.length;
                
                await new Promise(resolve => setTimeout(resolve, this.randomDelay(60, 150)));
                
                if (this.reportCount % 15 === 0) {
                    const successRate = ((this.successCount / this.reportCount) * 100).toFixed(1);
                    console.log(`\n📊 [ROTATION] Total: ${this.reportCount} | Success: ${successRate}% | Current: @${username}\n`);
                }
                
            } catch (error) {
                console.log(`🌀 Rotation Error: ${error.message}`);
                consecutiveErrors++;
                await new Promise(resolve => setTimeout(resolve, 5000));
            }
        }
    }

    // Show banner
    showBanner() {
        console.log(`
        ⠠⠤⠤⠤⠤⠤⣤⣤⣤⣄⣀⣀                        
             ⠉⠉⠛⠛⠿⢶⣤⣄⡀                  
  ⢀⣀⣀⣠⣤⣤⣴⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠿⠿⢿⡇                  
⠚⠛⠉⠉⠉      ⢀⣀⣀⣤⡴⠶⠶⠿⠿⠿⣧⡀   ⠤⢄⣀           
       ⢀⣠⡴⠞⠛⠉⠁       ⢸⣿⣷⣶⣦⣤⣄⣈⡑⢦⣀        [ OPEN JASA BANNED TIKTOK ] 
    ⣠⠔⠚⠉⠁          ⢀⣾⡿⠟⠉⠉⠉⠉⠙⠛⠿⣿⣮⣷⣤      AUTHOR : LORDHOZOO
                  ⢀⣿⡿⠁         ⠉⢻⣯⣧⡀      YT : LORDHOZOO
                  ⢸⣿⡇            ⠉⠻⢷⡤     TIKTOK : LORDHOZOO
                  ⠈⢿⣿⡀                    HARGA : 350K
                   ⠈⠻⣿⣦⣤⣀⡀                nomor : 628999859595
                      ⠉⠙⠛⠛⠻⠿⠿⣿⣶⣶⣦⣄⣀     
                            ⠉⠻⣿⣯⡛⠻⢦⡀  
                              ⠈⠙⢿⣆ ⠙⢆ 
                                ⠈⢻⣆ ⠈⢣
                                  ⠻⡆ ⠈
                                   ⢻⡀ 
                                   ⠈⠃     
╔══════════════════════════════════════════════════════════════╗
║ 🚀 TIKTOK AUTO-REPORT DENGAN TOKEN ASLI                    ║
║ 📍 API: ${REPORT_API_URL} ║
║ 👤 Reporter: ${REPORTER_NAME}                              ║
║ 📧 Email: ${EMAIL}                          ║
║ 🔑 Token: Real-time dari TikTok                            ║
╚══════════════════════════════════════════════════════════════╝
        `);
    }

    // Show report types
    showReportTypes() {
        console.log('\n📋 JENIS PELAPORAN:');
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
        console.log('1. 🚀 UNLIMITED - Satu target, report unlimited');
        console.log('2. 🔄 ROTATION - Multiple targets, rotating');
        console.log('3. 📊 STATISTICS');
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
                const usernamesInput = readline.question('Masukkan usernames (pisahkan koma): ');
                const usernames = usernamesInput.split(',')
                    .map(u => u.trim().replace('@', ''))
                    .filter(u => u.length > 0);
                
                if (usernames.length > 0) {
                    await this.startMultipleReports(usernames);
                } else {
                    console.log('❌ Tidak ada username valid!');
                    await this.showMenu();
                }
                break;
                
            case '3':
                this.showStatistics();
                await this.showMenu();
                break;
                
            case '4':
                console.log('👋 Keluar...');
                process.exit(0);
                break;
                
            default:
                console.log('❌ Pilihan tidak valid!');
                await this.showMenu();
        }
    }

    // Show statistics
    showStatistics() {
        console.log('\n📈 STATISTICS:');
        console.log(`   Total Reports: ${this.reportCount}`);
        console.log(`   Successful: ${this.successCount}`);
        console.log(`   Failed: ${this.failedCount}`);
        if (this.reportCount > 0) {
            const successRate = ((this.successCount / this.reportCount) * 100).toFixed(2);
            console.log(`   Success Rate: ${successRate}%`);
        }
        console.log(`   Running: ${this.isRunning ? 'YES' : 'NO'}`);
    }

    // Handle shutdown
    setupShutdownHandler() {
        process.on('SIGINT', () => {
            console.log('\n\n🛑 PROGRAM DIHENTIKAN');
            console.log('📊 FINAL STATISTICS:');
            this.showStatistics();
            console.log(`\n📧 Email: ${EMAIL}`);
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

// Run
console.log('🔧 Initializing TikTok Auto-Reporter dengan Token Asli...');
const autoReporter = new TikTokAutoReporter();
autoReporter.run().catch(console.error);
