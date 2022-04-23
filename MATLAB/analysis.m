% Define some constants
figure(1);
% figure(2);
% figure(3);
% figure(4);
% figure(5);

STEP =        [1,0,0,0,0];
RL =          [0,1,0,0,0];
BODE =        [0,0,1,0,0];
NYQUIST =     [0,0,0,1,0];
DISTURBANCE = [0,0,0,0,1];
DEFUALT = STEP + DISTURBANCE;

% % initial open loop analysis
% D0G = new_system(initG(), 'D0', STEP); % Add constants to have multiple outputs
% analyze_system(D0G);
% % % 
% % % % first iteration
% D1 = tf('s') + 3;
% D1G = new_system(initG(), D1, i, 'D1', STEPCL + RLOL + BODE + NYQUIST + DISTURBANCE);
% i = analyze_system(D1G);
% % % 
% % % % second iteration
% D2 = tf('s') + 0.1;
% D2G = new_system(initG(), D2, i, 'D2', STEPCL + RLOL + BODE + NYQUIST + DISTURBANCE);
% i = analyze_system(D2G);
% % 
% % % third iteration
% D3 = tf('s') + 0.001;
% D3G = new_system(initG(), D3, i, 'D3', STEPCL + RLOL + BODE + NYQUIST + DISTURBANCE);
% i = analyze_system(D3G);
% 
syms x;
figure(1);
fplot(heaviside(x));
grid on;
hold on;

D4 = (tf('s') + 0.01) * 5;
D4G = feedback(D4 * initG(), 1);%new_system(feedback(D4 * initG(), 1), 'D4', STEP);
plot_step(1, D4G);

Kp = 50;
Kd = 25;
Ki = 5;

D5 = (Kd * tf('s')) + Kp + (Ki/tf('s'));
D5G = feedback(D5 * initG(), 1);%new_system(feedback(D5 * initG(), 1), 'D5', STEP);
% analyze_system(D5G);
plot_step(1, D5G);
D6G = new_system(initSS(), 'D6', STEP);
% analyze_system(D6G);
D6G = initSS();
plot_step(1, D6G);
legend({'Step', 'D4', 'D5', 'D6'})

save_plots('D4-D5-D6-Comparison');

function analyze_system(data)
    title = data.title;
    sys = data.G;

    % plot step response
    if data.output(1) == 1
        plot_step(1, sys);
    end
    % plot root locus
    if data.output(2) == 1
        plot_rl(2, sys);
    end
    % plot bode
    if data.output(3) == 1
        plot_bode(3, sysol, data.opts);
    end
    % plot nyquist
    if data.output(4) == 1
        plot_nyquist(4, sysol, title);
    end
%     if data.output(5) == 1
%         W = data.G / (1 + data.D * data.G);
%         plot_impulse(7, W);
%     end
end

function save_plots(title)
    saveas(figure(1), strcat(title, '-Step.jpg'));
    saveas(figure(2), strcat(title, '-RL.jpg'));
    saveas(figure(3), strcat(title, '-Bode.jpg'));
    saveas(figure(4), strcat(title, '-Nyquist.jpg'));
    saveas(figure(5), strcat(title, '-Disturbance.jpg'));
end

function plot_step(i, sys)
    step(sys)
    grid on;
    hold on;
    stepinfo(sys)
end

function plot_rl(i, sys)
    rlocus(sys)
    grid on;
end

function plot_bode(i, sys, opts)
    bode(sys, opts)
    grid on;
end

function plot_nyquist(i, sys)
    nyquist(sys)
    grid on;
end

function plot_impulse(i, sys)
    impulse(sys)
    grid on;
end

function sys = new_system(G, title, output)
    % This function creates a struct of data
    % to be passed to an analytical function.
    % It helps keep track of different iterations
    % and results.

    % Set bode options to have
    bopts = bodeoptions;
    bopts.MagUnits = 'abs';
    bopts.MagScale = 'log';
    % Create the data object
    sys = struct();
    % Set the data
    sys.G = G;
    sys.opts = bopts;
    sys.title = title;
    sys.output = output;
end

function G = initSS()
    A = [0, 1;
         0 ,0];
    B = [0; 5*9.81/7];
    C = [1, 0];
    D = [0];
    Q = [100, 0;
         0 ,1];
    R = 0.1;
    K_new = lqr(A, B, Q, R);
    TT = [A, B; C, D];
    N = TT \ [zeros(1, length(A)) 1]';
    Nx = N(1:end-1);
    Nu = N(end);
    Nbar2 = Nu + K_new * Nx;

    Acl = A - B * K_new;
    Bcl = B * Nbar2;
    Ccl = C;
    Dcl = D;
    G = ss(Acl, Bcl, Ccl, Dcl);
end

function G = initG()
    % Create an open loop plant for our system
    s = tf ('s');
    G = 5*9.81 / (7*s^2);
end