fs=44100;
numtaps=2; %% Make this even, please.
ordvec=[0:numtaps-1]';
VA=flipud(vander(ordvec)');
iVA=inv(VA); %matrix to compute coefs
numplots=16;
for ind=1:numplots
eta=(ind-1)/(numplots-1); %% fractional delay
delay=eta+numtaps/2-1; %% keep fract. delay between two center taps
deltavec=(delay*ones(numtaps,1)).^ordvec;
b=iVA*deltavec;
[H,w]=freqz(b,1,2000);
b
ba= [(numplots-ind)/(numplots-1),((ind-1)/(numplots-1))];
ba'
figure(1)
subplot(2,1,1)
plot(w*fs/(2*pi),(abs(H)))
grid on
hold on
xlabel('Freq, Hz')
ylabel('magnitude')
axis([0 fs/2 0 1.1])
subplot(2,1,2)
plot(w*fs/(2*pi),180/pi*unwrap(angle(H)))
grid on
hold on
xlabel('Freq, Hz')
ylabel('phase')
xlim([0 fs/2])
end
figure(1)
subplot(2,1,1);hold off;
title('Lagrange Interpolator')
subplot(2,1,2);hold off;