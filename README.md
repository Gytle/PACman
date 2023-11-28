# PACman
Finding Phase-Amplitude Coupling events in continuous EEG recordings in an automatic manner

# Summary
Neuronal oscillation, a process where neurons communicate with rhythmic patterns, can be observed as waves in electroencephalographic (EEG) recordings of brain signals. This communication mode is a cost-efficient way to achieve various cognitive processes ranging from temporal binding of sensory inputs, attention selection to even memory consolidation. Recent developments in our understanding of neuronal oscillation suggest that the phase of slower oscillations can modulates the amplitude of faster neuronal oscillations, a phenomenon known as Phase-Amplitude Coupling (PAC). PAC can be observed in large part of the scalp with EEG and is a putative mechanism for distributing information among large-scale networks with implications for learning, memory consolidation and retrieval.

This project aims to develop an algorithm for detecting PAC events in continuous EEG recordings, focusing initially on the detection of slow-waves coupled with spindles since their co-occurrence is a well characterized phenomenon in sleep EEG and will serve as ‘ground-truth’ for the validation of the method. [...]
 The successful method will be adapted to be extend to the cross-coupling of any kind of frequency range, increasing the possibility of usage to a broader extent and answering new biological questions.

Understanding the relationship between phase and amplitude, such as in the case of slow waves and spindles, can be useful for evaluating sleep quality and may help identify abnormalities in sleep patterns. The coupling between spindles and slow waves is tightly linked to memory consolidation and analyzing their interaction contributes to understanding memory processing and retention. Investigating abnormalities in phase-amplitude coupling can also provide insights into disorders such as Alzheimer’s disease, epilepsy and schizophrenia, and be used as potential biomarkers. Moreover understanding neural synchronization patterns can contribute to the development of BCIs and neurofeedback systems

Despite its relatively easy implementation, this project offers the possibility to answer relevant biological questions. The cross-coupling of brainwaves represents an interesting and yet poorly investigated strategy by which the brain operates and may reveal important physiological mechanisms. For instance, it has been shown that the coupling of slow-waves and spindle is tightly related to hippocampal ripples (which otherwise would not be observable through non-invasive techniques).


# Literature

Scientific framework of neuronal oscillations and phase-amplitude coupling:

Buzsáki, G., & Draguhn, A. (2004). Neuronal Oscillations in Cortical Networks. Science, 304(5679), 1926–1929. https://doi.org/10.1126/science.1099745

Canolty, R. T., & Knight, R. T. (2010). The functional role of cross-frequency coupling. Trends in Cognitive Sciences, 14(11), 506–515. https://doi.org/10.1016/j.tics.2010.09.001


Methods for Phase-Amplitude Coupling identification:

Canolty, R. T., Edwards, E., Dalal, S. S., Soltani, M., Nagarajan, S. S., Kirsch, H. E., Berger, M. S., Barbaro, N. M., & Knight, R. T. (2006). High Gamma Power Is Phase-Locked to Theta Oscillations in Human Neocortex. Science, 313(5793), 1626–1628. https://doi.org/10.1126/science.1128115

Tort, A. B. L., Komorowski, R., Eichenbaum, H., & Kopell, N. (2010). Measuring Phase-Amplitude Coupling Between Neuronal Oscillations of Different Frequencies. Journal of Neurophysiology, 104(2), 1195–1210. https://doi.org/10.1152/jn.00106.2010

Penny, W. D., Duzel, E., Miller, K. J., & Ojemann, J. G. (2008). Testing for nested oscillation. Journal of Neuroscience Methods, 174(1), 50–61. https://doi.org/10.1016/j.jneumeth.2008.06.035

Dupré la Tour, T., Tallot, L., Grabot, L., Doyère, V., Wassenhove, V. van, Grenier, Y., & Gramfort, A. (2017). Non-linear auto-regressive models for cross-frequency coupling in neural time series. PLOS Computational Biology, 13(12), e1005893. https://doi.org/10.1371/journal.pcbi.1005893

Munia, T. T. K., & Aviyente, S. (2019). Time-Frequency Based Phase-Amplitude Coupling Measure For Neuronal Oscillations. Scientific Reports, 9(1), Article 1. https://doi.org/10.1038/s41598-019-48870-2

Samiee, S., & Baillet, S. (2017). Time-resolved phase-amplitude coupling in neural oscillations. NeuroImage, 159, 270–279. https://doi.org/10.1016/j.neuroimage.2017.07.051
Soulat, H., Stephen, E. P., Beck, A. M., & Purdon, P. L. (2022). State space methods for phase amplitude coupling analysis. Scientific Reports, 12(1), Article 1. https://doi.org/10.1038/s41598-022-18475-3
