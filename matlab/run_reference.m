function result = run_reference(seed, num_bits, output_path)
% Corrected, toolbox-free BPSK/QPSK reference; Es=1 and Eb/N0 per bit.
% MATLAB: run_reference(17, 400000, 'reports/matlab_ber.csv')
% Octave: addpath('matlab'); run_reference(17, 400000, 'reports/matlab_ber.csv')
  if nargin < 1, seed = 17; end
  if nargin < 2, num_bits = 400000; end
  if nargin < 3, output_path = 'reports/matlab_ber.csv'; end
  assert(num_bits >= 2 && mod(num_bits, 2) == 0, 'Use an even bit count');
  rng(seed, 'twister');
  ebn0_db = 0:2:8;
  result = zeros(length(ebn0_db), 4);
  for i = 1:length(ebn0_db)
    gamma = 10^(ebn0_db(i)/10);
    bits = randi([0 1], num_bits, 1);
    bpsk = 2*bits - 1;
    received_b = bpsk + sqrt(1/(2*gamma))*randn(num_bits, 1);
    bpsk_ber = mean((received_b > 0) ~= bits);
    pairs = reshape(bits, 2, []).';
    qpsk = ((2*pairs(:,1)-1) + 1j*(2*pairs(:,2)-1))/sqrt(2);
    received_q = qpsk + sqrt(1/(4*gamma))* ...
      (randn(size(qpsk)) + 1j*randn(size(qpsk)));
    decisions = [real(received_q)>0, imag(received_q)>0];
    decoded = reshape(decisions.', [], 1);
    qpsk_ber = mean(decoded ~= bits);
    theory = 0.5*erfc(sqrt(gamma));
    tolerance = 6*sqrt(theory*(1-theory)/num_bits) + 6/num_bits;
    assert(abs(bpsk_ber-theory) <= tolerance, 'BPSK disagrees with theory');
    assert(abs(qpsk_ber-theory) <= tolerance, 'QPSK disagrees with theory');
    result(i,:) = [ebn0_db(i), bpsk_ber, qpsk_ber, theory];
  end
  fid = fopen(output_path, 'w');
  assert(fid >= 0, 'Cannot open output path; create its parent directory');
  cleanup = onCleanup(@() fclose(fid));
  fprintf(fid, 'ebn0_db,bpsk_ber,qpsk_ber,theory\n');
  fprintf(fid, '%.12g,%.12g,%.12g,%.12g\n', result.');
end
