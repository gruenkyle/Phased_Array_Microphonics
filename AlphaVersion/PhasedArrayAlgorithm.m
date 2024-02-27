%{
This is the Phased Array Algorithm I wrote for GrayUR undergraduate 
Research during the year of Fall 2023. The main goal is to create a closed
environment that uses synthetic audio signals that can be manipulated 
by our phased array algo that will later be transferred into python code.
%}

%FIELDS - Signal Durations / Unchanged Variables
SOUND_SPEED = 343; % m/s
FS = 44100; % Sample Rate
CYCLES = 1; % Cycles of Wave
DURATION_OF_SIGNAL = CYCLES * (1/440); % Duration of Signal Wave
T = 0:1/FS:DURATION_OF_SIGNAL; % Time Vector

%Phased Array System Information 
TOTAL_SPREAD = 10.00000001; % Spread of Array in Meters
MIC_COUNT = 3; % Total Number of Microphones
CENTER = TOTAL_SPREAD / 2; % Center of System

% Types of Input Sound Signals 
SMALLINPUTSIG = sin(2*pi*1000*T); % 1kHz
MEDIUMINPUTSIG = sin(2*pi*1700*T); % 1.7 kHz
LARGEINPUTSIG = sin(2*pi*2430*T); % 2.43 kHz

% Use this variable too much to not make it
forLoopArr = 1:MIC_COUNT;



%{ Target Marker in Comparison to System 
%                  C
%     A --- B --- SYS --- D --- E
%                  |
%                SysAdj 
%                  | - - - SysOpp - O 
%}

SystemAdjacentDisO = 10; % Distance Adjacent to System Meters - Target
SystemOppositeDisO = 2.5; % Distance Opposite to System Meters - Target

SystemAdjacentDisX = 5; % Distance Opposite to System For Off Sound
SystemOppositeDisX = -2.5; % Distance Opposite to System For Off Sound


% Check Orientation of Target (Negative or Positive)
% Used in later calculations of distance 

OrientationO = "R"; % Assumed to be on Right Side of System
OrientationX = "R"; % Assumed to be on Right Side of System

if (SystemOppositeDisO < 0)
    OrientationO = "L"; % Negative Opp Value so Left Side of System
    SystemOppositeDisO = abs(SystemOppositeDisO);
end

if (SystemOppositeDisX < 0)
    OrientationX = "L"; % Negative Opp Value so Left Side of System
    SystemOppositeDisX = abs(SystemOppositeDisX);
end

% Calculate Distances of Target Sound to Microphones

MIC_DISTANCES_TO_CENTER = zeros(1, MIC_COUNT);
STARTDIS = 0;

for micIndex = forLoopArr
    % Calculate the distance from the center for each microphone
    MIC_DISTANCES_TO_CENTER(micIndex) = (micIndex - 1 - (MIC_COUNT - 1) / 2) * (TOTAL_SPREAD / (MIC_COUNT - 1));
end

%Turns all distances from microphones to system into positive numbers
MIC_DISTANCES_TO_CENTER = abs(MIC_DISTANCES_TO_CENTER);

%Initialize all Distance Arrays to zero 

MIC_DISTANCE_O = zeros(1, MIC_COUNT);
DISTANCE_O = zeros(1, MIC_COUNT);

MIC_DISTANCE_X = zeros(1, MIC_COUNT);
DISTANCE_X = zeros(1, MIC_COUNT);

% Calculate Distance to On Sound
for OnS = forLoopArr
    if (OrientationO == "R")
        if (OnS < (MIC_COUNT / 2))
            MIC_DISTANCE_O(OnS) = MIC_DISTANCES_TO_CENTER(OnS) + SystemOppositeDisO;
            DISTANCE_O(OnS) = sqrt(MIC_DISTANCE_O(OnS)^2 + SystemAdjacentDisO^2);
        else
            MIC_DISTANCE_O(OnS) = abs(SystemOppositeDisO - MIC_DISTANCES_TO_CENTER(OnS));
            DISTANCE_O(OnS) = sqrt(MIC_DISTANCE_O(OnS)^2 + SystemAdjacentDisO^2);
        end
    end
    if (OrientationO == "L")
        if (OnS > (MIC_COUNT / 2))
            MIC_DISTANCE_O(OnS) = MIC_DISTANCES_TO_CENTER(OnS) + SystemOppositeDisO;
            DISTANCE_O(OnS) = sqrt(MIC_DISTANCE_O(OnS)^2 + SystemAdjacentDisO^2);
        else
            MIC_DISTANCE_O(OnS) = abs(SystemOppositeDisO - MIC_DISTANCES_TO_CENTER(OnS));
            DISTANCE_O(OnS) = sqrt(MIC_DISTANCE_O(OnS)^2 + SystemAdjacentDisO^2);
        end
    end
end

% Calculate Distances to Off Sounds
for OffS = forLoopArr
    if (OrientationX == "L")
        if (OffS > (MIC_COUNT / 2))
            MIC_DISTANCE_X(OffS) = MIC_DISTANCES_TO_CENTER(OffS) + SystemOppositeDisX;
            DISTANCE_X(OffS) = sqrt(MIC_DISTANCE_X(OffS)^2 + SystemAdjacentDisX^2);
        else
            MIC_DISTANCE_X(OffS) = abs(SystemOppositeDisX - MIC_DISTANCES_TO_CENTER(OffS));
            DISTANCE_X(OffS) = sqrt(MIC_DISTANCE_X(OffS)^2 + SystemAdjacentDisX^2);
        end
    end
    if (OrientationX == "R")
        if (OffS < (MIC_COUNT / 2))
            MIC_DISTANCE_X(OffS) = MIC_DISTANCES_TO_CENTER(OffS) + SystemOppositeDisX;
            DISTANCE_X(OffS) = sqrt(MIC_DISTANCE_X(OffS)^2 + SystemAdjacentDisO^2);
        else
            MIC_DISTANCE_X(OffS) = abs(SystemOppositeDisX - MIC_DISTANCES_TO_CENTER(OffS));
            DISTANCE_X(OffS) = sqrt(MIC_DISTANCE_X(OffS)^2 + SystemAdjacentDisO^2);
        end
    end
end

% Find Furthest and Closest Mic
[minDistance, closestIndex] = min(DISTANCE_O);
[maxDistance, furthestIndex] = max(DISTANCE_O);

%Find Delay and Sample Delay for each Microphone (SOUND O)
delayOi = zeros(1, MIC_COUNT);
delayOiSample = zeros(1, MIC_COUNT);

%Find Delay and SampleDelay for each Microphone (SOUND X)
delayXi = zeros(1, MIC_COUNT);
delayXiSample = zeros(1, MIC_COUNT);

for i = forLoopArr
    delayOi(i) = (DISTANCE_O(i) / SOUND_SPEED);
    delayOiSample(i) = round(delayOi(i) * FS);

    delayXi(i) = (DISTANCE_X(i) / SOUND_SPEED);
    delayXiSample(i) = round(delayXi(i) * FS);
end

%Find Total Sample Delay in Relation to the Furthest Mic (SOUND O)
totalSampleDelayOi = zeros(1, MIC_COUNT);

for j = forLoopArr
    totalSampleDelayOi(j) = round (delayOiSample(furthestIndex) - delayOiSample(j));
    totalSampleDelayOi(j) = abs(totalSampleDelayOi(j));
end


% Create Signal Wave Arrays in Cells
micSignalCells = cell(1,MIC_COUNT);
maxLengths = zeros(1, MIC_COUNT);

for initial = forLoopArr
    microphoneSignal = zeros(1,1);
    micSignalCells{initial} = microphoneSignal;
end

% Create Synthetic Audio Signals with Proper Delays 
% This is in relation to the microphone (SOUND X)
for offSound = forLoopArr
    micSignalCells{offSound} = [zeros(1, delayXiSample(offSound)), SMALLINPUTSIG];
    maxLengths(offSound) = length(micSignalCells{offSound});
end

maxSize = max(maxLengths);
offMaxIndex = maxSize;

for off = forLoopArr
    micSignalCells{off} = [micSignalCells{off}, zeros(1, maxSize - maxLengths(off))];
end

% Create Synthetic Audio Signals with Proper Delays 
% This is in relation to the microphone (SOUND O)

for k = forLoopArr
    micSignalCells{k} = [micSignalCells{k}, zeros(1, delayOiSample(k))];
    micSignalCells{k} = [micSignalCells{k}, LARGEINPUTSIG];
    micSignalCells{k} = [micSignalCells{k}, zeros(1,20)];
    maxLengths(k) = length(micSignalCells{k});
end

% Set all array lengths to the same size to plot
maxSize = max(maxLengths);
targetMaxIndex = maxSize;

for y = forLoopArr
    micSignalCells{y} = [micSignalCells{y}, zeros(1, maxSize - maxLengths(y))];
end

% Plot Signals on a graph
colors = {'g', 'r', 'b', 'm', 'c', 'y'};
subplot(2,2,1);

for plot1 = forLoopArr
    plot(1/FS:1/FS:maxSize/FS, micSignalCells{plot1}, colors{plot1});
    hold on;
end
title('Microphone Signals No Changes');
ylim([-3,3]);


% Set Delay on microphones to match furthest Index

for delayLoopI = forLoopArr
    if(delayLoopI ~= furthestIndex)
        micSignalCells{delayLoopI} = [zeros(1, ceil(totalSampleDelayOi(delayLoopI))), micSignalCells{delayLoopI}];
    end
    maxLengths(delayLoopI) = length(micSignalCells{delayLoopI});
end

maxSize = max(maxLengths);

% Add zeros to end of smaller arrays to match largest size

for delayLoopII = forLoopArr
    micSignalCells{delayLoopII} = [micSignalCells{delayLoopII}, zeros(1, maxSize - maxLengths(delayLoopII))];
end

% Plot Mic Signals with delay included for O sound
subplot(2,2,2);

for plot2 = forLoopArr
    plot(1/FS:1/FS:maxSize/FS, micSignalCells{plot2}, colors{plot2});
    hold on;
end
title('Microphone Signals With Delay O');
ylim([-3,3]);

% Sum both Signals to get final signal
micSumSignal = zeros(1,1);

for finalSum = forLoopArr
    micSumSignal = micSumSignal + micSignalCells{finalSum};
end

subplot(2,2,3);

for plot3 = forLoopArr
    plot(1/FS:1/FS:maxSize/FS, micSumSignal, 'black');
    hold on;
end
title('Final Summation Wave');
ylim([-3,3]);

offMax = max(micSumSignal(1:offMaxIndex));
tarMax = max(micSumSignal(offMaxIndex:targetMaxIndex));
