% Define some constants
i = 1;
STEPOL = [1,0,0,0,0,0,0];
STEPCL = [0,1,0,0,0,0,0];
RLOL = [0,0,1,0,0,0,0];
RLCL = [0,0,0,1,0,0,0];
BODE = [0,0,0,0,1,0,0];
NYQUIST = [0,0,0,0,0,1,0];
DISTURBANCE = [0,0,0,0,0,0,1];

% % initial open loop analysis
% D0G = new_system(initG(), 1, i, 'D0', STEPOL + RLOL + BODE + NYQUIST + DISTURBANCE); % Add constants to have multiple outputs
% i = analyze_system(D0G);
% 
% % first iteration
% D1 = tf('s') + 3;
% D1G = new_system(initG(), D1, i, 'D1', STEPCL + RLCL + DISTURBANCE);
% i = analyze_system(D1G);
% 
% % second iteration
% D2 = tf('s') + 0.1;
% D2G = new_system(initG(), D2, i, 'D2', STEPCL + RLCL + DISTURBANCE);
% i = analyze_system(D2G);
% 
% % third iteration
D3 = tf('s') + 0.001;
D3G = new_system(initG(), D3, i, 'D3', STEPCL + RLCL + DISTURBANCE + BODE + NYQUIST);
i = analyze_system(D3G);

D4 = (tf('s') + 0.01) * 5;
sample = new_system(initG(), D4, i, 'D4', STEPCL + RLCL + DISTURBANCE);
i = analyze_system(sample);

function i = analyze_system(data)
    i = data.fign;
    title = data.title;
    sysol = data.G;
    syscl = feedback(data.D * data.G, 1);

    % plot step response
    if data.olstep == 1
        plot_step(i, sysol, strcat(title, '-OL'));
        i = i + 1;
    end
    if data.clstep == 1
        plot_step(i, syscl, strcat(title, '-CL'));
        i = i + 1;
    end
    % plot root locus
    if data.olrl == 1
        plot_rl(i, sysol, strcat(title, '-OL'));
        i = i + 1;
    end
    if data.clrl == 1
        plot_rl(i, syscl, strcat(title, '-CL'));
        i = i + 1;
    end
    % plot bode
    if data.bode == 1
        plot_bode(i, sysol, title);
        i = i + 1;
    end
    % plot nyquist
    if data.nyquist == 1
        plot_nyquist(i, sysol, title);
        i = i + 1;
    end
    if data.disturbance == 1
        W = data.G / (1 + data.D * data.G);
        plot_impulse(i, W, strcat(title, '-Disturbance'));
        i = i + 1;
    end
end

function plot_step(i, sys, title)
    figure(i)
    step(sys)
    saveas(figure(i), strcat(title, '-Step.jpg'));
    disp(title);
    stepinfo(sys)
end

function plot_rl(i, sys, title)
    figure(i)
    rlocus(sys)
    grid on;
    saveas(figure(i), strcat(title, '-RL.jpg'));
end

function plot_bode(i, sys, title)
    figure(i)
    bode(sys)
    saveas(figure(i), strcat(title, '-Bode.jpg'));
end

function plot_nyquist(i, sys, title)
    figure(i)
    nyquist(sys)
    saveas(figure(i), strcat(title, '-Nyquist.jpg'));
end

function plot_impulse(i, sys, title)
    figure(i)
    impulse(sys)
    saveas(figure(i), strcat(title, '-Impulse.jpg'));
end

function sys = new_system(G, D, i, title, output)
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
    sys.D = D;
    sys.fign = i;
    sys.opts = bopts;
    sys.title = title;

    if length(output) < 7
        sys.olstep = 0;
        sys.clstep = 0;
        sys.olrl = 0;
        sys.clrl = 0;
        sys.bode = 0;
        sys.nyquist = 0;
        sys.disturbance = 0;
    else
        sys.olstep = output(1);
        sys.clstep = output(2);
        sys.olrl = output(3);
        sys.clrl = output(4);
        sys.bode = output(5);
        sys.nyquist = output(6);
        sys.disturbance = output(7);
    end

    sys.output = output;
end

function G = initG()
    % Create an open loop plant for our system
    s = tf ('s');
    G = 5*9.81 / (7*s^2);
end