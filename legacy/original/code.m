% Simulation of Digital Communication System

clc; clear; close all;

% Parameters
numBits = 1e5; % Number of bits
Eb_N0_dB = 0:2:14; % SNR range in dB
M_BPSK = 2; % BPSK modulation order
M_QPSK = 4; % QPSK modulation order

% Generate random binary data
data = randi([0 1], numBits, 1);

% BPSK Modulation
bpskMod = 2*data - 1;

% QPSK Modulation
qpskSymbols = reshape(data, [], 2);
qpskMod = (2*qpskSymbols(:,1) - 1) + 1j * (2*qpskSymbols(:,2) - 1);

% BER Analysis
BER_BPSK = zeros(size(Eb_N0_dB));
BER_QPSK = zeros(size(Eb_N0_dB));

for i = 1:length(Eb_N0_dB)
    % Convert Eb/N0 to SNR
    SNR = Eb_N0_dB(i) + 10*log10(log2(M_BPSK));
    noise = sqrt(1/(2*(10^(SNR/10)))) * (randn(size(bpskMod)) + 1j*randn(size(bpskMod)));
    rxBPSK = bpskMod + noise;
    
    % BPSK Demodulation
    bpskDemod = real(rxBPSK) > 0;
    BER_BPSK(i) = sum(bpskDemod ~= data) / numBits;
    
    % QPSK
    SNR = Eb_N0_dB(i) + 10*log10(log2(M_QPSK));
    noise = sqrt(1/(2*(10^(SNR/10)))) * (randn(size(qpskMod)) + 1j*randn(size(qpskMod)));
    rxQPSK = qpskMod + noise;
    
    % QPSK Demodulation
    qpskDemod = [real(rxQPSK) > 0, imag(rxQPSK) > 0];
    BER_QPSK(i) = sum(qpskDemod(:) ~= data) / numBits;
end

% Theoretical BER
BER_theory_BPSK = qfunc(sqrt(2 * (10.^(Eb_N0_dB/10))));
BER_theory_QPSK = qfunc(sqrt(10.^(Eb_N0_dB/10)));

% Plot results
figure;
semilogy(Eb_N0_dB, BER_BPSK, 'ro-', 'LineWidth', 2);
hold on;
semilogy(Eb_N0_dB, BER_QPSK, 'bs-', 'LineWidth', 2);
semilogy(Eb_N0_dB, BER_theory_BPSK, 'r--', 'LineWidth', 2);
semilogy(Eb_N0_dB, BER_theory_QPSK, 'b--', 'LineWidth', 2);
hold off;
legend('Simulated BPSK', 'Simulated QPSK', 'Theoretical BPSK', 'Theoretical QPSK');
xlabel('E_b/N_0 (dB)');
ylabel('Bit Error Rate');
grid on;
title('BER Performance of BPSK and QPSK');
